import os
import json
import numpy as np

from pdf2image import convert_from_path
from src.image.processor import process_image
from src.invoice.tool import extract_roi_info, estimate_frame_rotation, get_pdf_type, search_specific_info
from utils.google_ocr import GoogleVisionAPI
from utils.folder_file_manager import log_print
from utils.type_model import TYPE_INFO
from settings import CUR_DIR


class InvoiceExtractor:
    def __init__(self):
        self.google_api = GoogleVisionAPI()
        self.field_info = None
        self.pdf_type = None

    @staticmethod
    def correct_volme_gewicht(content):
        content = content.replace(" ", "")
        if content[0] == ",":
            content = content[1:]
        comma_index = content.find(",")
        if -1 < comma_index < len(content) - 2:
            new_content = content[max(comma_index - 2, 0):comma_index + 3]
            if not new_content[-1].isdigit():
                new_content = new_content[:-1]
        else:
            m_index = content.find("m")
            new_content = content[:m_index - 2] + "," + content[m_index - 2:m_index]

        return new_content

    def get_raw_data_from_api(self, img_path, file_name, dir_name):
        raw_data = None
        for i in range(3):
            raw_data = self.google_api.detect_text(img_path=img_path, file_name=file_name, dir_name=dir_name)
            if raw_data is not None:
                break
        return raw_data

    def run(self, pdf_path, pdf_file_name, dir_name=None):
        self.field_info = {"Barcode": "", "Lieferschein_Nr": "", "DTS_Date": "", "DTS_Time": "", "Gewicht": "",
                           "Volume": "", "Fuhre": ""}
        pdf_frame = [np.array(page) for page in convert_from_path(pdf_path, 200)][0]
        pdf_frame_path = process_image(frame=pdf_frame, file_name=pdf_file_name)

        if os.path.exists(os.path.join(CUR_DIR, 'test_json', f"temp_{dir_name}_{pdf_file_name}.json")):
            with open(os.path.join(CUR_DIR, 'test_json', f"temp_{dir_name}_{pdf_file_name}.json")) as f:
                ocr_result = json.load(f)
        else:
            ocr_result = self.get_raw_data_from_api(img_path=pdf_frame_path, file_name=pdf_file_name,
                                                    dir_name=dir_name)
        rotated_estimation = estimate_frame_rotation(json_result=ocr_result)
        if rotated_estimation is not None:
            pdf_frame_path = process_image(frame=pdf_frame, file_name=pdf_file_name, rotation_result=rotated_estimation)
            ocr_result = self.google_api.detect_text(img_path=pdf_frame_path, file_name=pdf_file_name,
                                                     dir_name=dir_name)

        self.pdf_type = get_pdf_type(text_info=ocr_result)
        if self.pdf_type == "type10":
            pdf_frame_path = process_image(frame=pdf_frame, file_name=pdf_file_name, thresh_noise=4)
            ocr_result = self.get_raw_data_from_api(img_path=pdf_frame_path, file_name=pdf_file_name,
                                                    dir_name=dir_name)
        if self.pdf_type == "type3":
            self.pdf_type = "type1"

        self.field_info = self.extract_info_from_json(json_result=ocr_result)
        self.field_info = self.correct_extraction_result()

        return self.field_info

    def extract_info_from_json(self, json_result):
        json_width = json_result["textAnnotations"][0]["boundingPoly"]["vertices"][1]["x"]
        text_info = json_result["textAnnotations"][1:]
        if self.pdf_type == "type11":
            for i, t_info in enumerate(text_info):
                for k, t_coord in enumerate(t_info["boundingPoly"]["vertices"]):
                    if "y" not in t_coord.keys():
                        text_info[i]["boundingPoly"]["vertices"][k]["y"] = 0
            if not search_specific_info(json_result=text_info, search_word=["Zeit", "Zelt"]):
                self.pdf_type = "type11_B"
        elif self.pdf_type == "type7":
            if not search_specific_info(json_result=text_info, search_word=["Anwendung"]):
                self.pdf_type = "type7_B"

        type_model_info = TYPE_INFO[self.pdf_type]

        for i, t_info in enumerate(text_info):
            try:
                t_info_vertices = t_info["boundingPoly"]["vertices"]
                t_left = t_info_vertices[0]["x"]
                t_right = t_info_vertices[1]["x"]
                t_top = t_info_vertices[0]["y"]
                t_bottom = t_info_vertices[2]["y"]
                t_width = t_right - t_left
                t_height = t_bottom - t_top
                t_des = t_info["description"]
                if "Kies" in t_des:
                    if t_des.replace("Kies", "").isdigit() and self.field_info["Barcode"] == "":
                        self.field_info["Barcode"] = t_des
                for type_key in type_model_info.keys():
                    sub_type_info = type_model_info[type_key]
                    if t_des in sub_type_info["search_word"] and self.field_info[type_key] == "":
                        if (self.pdf_type == "type4" and type_key == "Lieferschein_Nr") and \
                                (text_info[i + 1]["description"] != "-" or text_info[i + 2]["description"] != "Nr"):
                            continue
                        if (self.pdf_type == "type5" or self.pdf_type == "type11") and type_key == "Lieferschein_Nr" \
                                and t_right < 0.5 * json_width:
                            continue
                        self.field_info[type_key] = \
                            extract_roi_info(json_result=text_info[:i] + text_info[i + 1:],
                                             roi_left=eval(sub_type_info["left"]), pdf_type=self.pdf_type,
                                             roi_right=eval(sub_type_info["right"]), roi_top=eval(sub_type_info["top"]),
                                             roi_bottom=eval(sub_type_info["bottom"]), label=type_key)
                if t_width > t_height:
                    pass
            except Exception as e:
                log_print(info_str=e)
                # print(e)
                if (self.pdf_type == "type11" or self.pdf_type == "type11_B") and \
                        t_info["description"] in ["Lleterscheln", "Lieferschein"]:
                    self.field_info["Lieferschein_Nr"] = \
                        extract_roi_info(json_result=text_info[i + 1:],
                                         roi_left=t_info["boundingPoly"]["vertices"][2]["x"],
                                         roi_right=2 * t_info["boundingPoly"]["vertices"][2]["x"] - t_info
                                         ["boundingPoly"]["vertices"][3]["x"],
                                         roi_top=-2, roi_bottom=1.2 * t_info["boundingPoly"]["vertices"][2]["y"],
                                         y_top=1, label="Lieferschein_Nr", pdf_type=self.pdf_type)
        self.field_info["Volume"] = self.field_info["Volume"].replace(".", ",")
        self.field_info["Gewicht"] = self.field_info["Gewicht"].replace(".", ",")

        return self.field_info

    def correct_extraction_result(self):
        if self.pdf_type == "type1":
            self.field_info["Volume"] = self.correct_volme_gewicht(content=self.field_info["Volume"])
            self.field_info["Volume"] = self.field_info["Volume"].replace("B", "8")
            self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
            self.field_info["Gewicht"] = self.field_info["Gewicht"].replace("B", "8")
            self.field_info["Gewicht"] = self.field_info["Gewicht"].replace("-", "")
            self.field_info["DTS_Time"] = self.field_info["DTS_Time"].replace(".", "")
            self.field_info["DTS_Date"] = self.field_info["DTS_Date"].replace("coco", "2020").replace(",", ".")
            self.field_info["DTS_Date"] = \
                self.field_info["DTS_Date"][max(self.field_info["DTS_Date"].find(".") - 2, 0):]
        elif self.pdf_type == "type2":
            if "ca" in self.field_info["Gewicht"]:
                ca_index = self.field_info["Gewicht"].find("ca")
                self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"][:ca_index])
                self.field_info["Volume"] = \
                    self.correct_volme_gewicht(content=self.field_info["Gewicht"][ca_index + 3:])
            else:
                self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
                ca_index = self.field_info["Volume"].find("ca")
                self.field_info["Volume"] = \
                    self.correct_volme_gewicht(content=self.field_info["Volume"][ca_index + 3:])
        elif self.pdf_type == "type4":
            if "t" in self.field_info["Volume"] and "m" in self.field_info["Gewicht"]:
                init_volume = self.field_info["Volume"]
                self.field_info["Volume"] = self.field_info["Gewicht"]
                self.field_info["Gewicht"] = init_volume
            self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
            self.field_info["Gewicht"] = self.field_info["Gewicht"].replace(":", "")
            self.field_info["Volume"] = self.correct_volme_gewicht(content=self.field_info["Volume"])
        elif self.pdf_type == "type5":
            fst_pt = self.field_info["DTS_Date"].find(".")
            col_pt = self.field_info["DTS_Date"].find(":")
            self.field_info["DTS_Date"], self.field_info["DTS_Time"] = \
                self.field_info["DTS_Date"][max(fst_pt - 2, 0):col_pt + 3].split(" ")
            new_gewicht = ""
            for g_c in self.field_info["Gewicht"]:
                if g_c.isdigit():
                    new_gewicht += g_c
            self.field_info["Gewicht"] = new_gewicht
            if len(self.field_info["Gewicht"]) > 5:
                self.field_info["Gewicht"] = self.field_info["Gewicht"].replace(self.field_info["Gewicht"][2], "")
            self.field_info["Lieferschein_Nr"] = \
                self.field_info["Lieferschein_Nr"].replace("Camion", "").replace(".", "").replace("/", "")
            self.field_info["Lieferschein_Nr"] = self.field_info["Lieferschein_Nr"].replace("N", "")
        elif self.pdf_type == "type6":
            self.field_info["DTS_Date"], self.field_info["DTS_Time"] = self.field_info["DTS_Date"].split("/")
            self.field_info["Lieferschein_Nr"] = self.field_info["Lieferschein_Nr"].replace(")", "")
            self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
        elif self.pdf_type == "type7":
            time_index = self.field_info["DTS_Date"].find(":")
            self.field_info["Lieferschein_Nr"] = self.field_info["Lieferschein_Nr"].replace("B", "8")
            self.field_info["DTS_Time"] = self.field_info["DTS_Date"][time_index - 2:].replace(" ", "")
            self.field_info["DTS_Date"] = self.field_info["DTS_Date"][:time_index - 2].replace(" ", "")
            self.field_info["Volume"] = self.correct_volme_gewicht(content=self.field_info["Volume"])
            self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
        elif self.pdf_type == "type7_B":
            self.field_info["Volume"] = self.field_info["Volume"].replace("E", "").replace(".", ",").replace(":", ",")
            self.field_info["Volume"] = self.correct_volme_gewicht(content=self.field_info["Volume"])
        elif self.pdf_type == "type8":
            self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
            self.field_info["Lieferschein_Nr"] = self.field_info["Lieferschein_Nr"].replace(".", "")
        elif self.pdf_type == "type9":
            self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
        elif self.pdf_type == "type10":
            self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
        elif self.pdf_type == "type11":
            self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
        elif self.pdf_type == "type12":
            self.field_info["Gewicht"] = self.field_info["Gewicht"].replace("'", ",")
            self.field_info["Gewicht"] = self.correct_volme_gewicht(content=self.field_info["Gewicht"])
            self.field_info["DTS_Time"] = self.field_info["DTS_Time"].replace("Uhr", "").replace("kg", "")
        self.field_info["DTS_Time"] = self.field_info["DTS_Time"].replace("(", "").replace(" ", "")
        self.field_info["DTS_Date"] = self.field_info["DTS_Date"].replace(" ", "")
        self.field_info["Lieferschein_Nr"] = self.field_info["Lieferschein_Nr"].replace(" ", "")

        return self.field_info


if __name__ == '__main__':
    import glob

    invoice_ext = InvoiceExtractor()
    invoice_ext.run(pdf_path="",
                    pdf_file_name="", dir_name="")
    # for j in range(12):
    j = 11
    for p_path in glob.glob(os.path.join(f"{j + 1}", "*.pdf"))[:10]:
        invoice_ext.run(pdf_path=p_path, dir_name=f"type{j + 1}", pdf_file_name="")

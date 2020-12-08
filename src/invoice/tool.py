from utils.type_model import TYPE
from utils.folder_file_manager import log_print
from settings import ROTATION_Y_THREAD, Y_BIND_THREAD


def extract_roi_info(json_result, roi_left, roi_right, roi_top, roi_bottom, pdf_type, y_top=None, label=None):
    roi_info = []
    roi_info_txt = ""
    for j_info in json_result:
        try:
            if label == "Lieferschein Nr" and not j_info["description"].replace("-", "").isdigit():
                continue
            if pdf_type == "type7_B" and label == "Volume" and j_info["description"].isalpha():
                continue
            if pdf_type == "type11" and label == "Lieferschein Nr" and j_info["description"] == "8404":
                continue
            if roi_left <= j_info["boundingPoly"]["vertices"][0]["x"] < roi_right and \
                    roi_top <= j_info["boundingPoly"]["vertices"][0]["y"] < roi_bottom:
                roi_info.append(j_info)
        except Exception as e:
            # print(e)
            log_print(info_str=e)
            if y_top is not None:
                if roi_left <= j_info["boundingPoly"]["vertices"][0]["x"] < roi_right and \
                        roi_top < y_top <= roi_bottom:
                    roi_info.append(j_info)
    sorted_y_roi_info = sorted(roi_info, key=lambda k: k["boundingPoly"]["vertices"][0]["y"])
    bind_y_close = []
    tmp_line = []
    init_value = sorted_y_roi_info[0]["boundingPoly"]["vertices"][0]["y"]
    for s_y_info in sorted_y_roi_info:
        if abs(init_value - s_y_info["boundingPoly"]["vertices"][0]["y"]) < Y_BIND_THREAD:
            tmp_line.append(s_y_info)
        else:
            bind_y_close.append(tmp_line[:])
            tmp_line.clear()
            tmp_line.append(s_y_info)
            init_value = s_y_info["boundingPoly"]["vertices"][0]["y"]

    bind_y_close.append(tmp_line[:])

    for b_y_info in bind_y_close:
        sorted_x_info = sorted(b_y_info, key=lambda k: k["boundingPoly"]["vertices"][0]["x"])
        if pdf_type == "type5" and label == "DTS_Date":
            ret_date = False
            for candi in sorted_x_info:
                if ":" in candi["description"]:
                    ret_date = True
                    break
            if not ret_date:
                continue
        for candi in sorted_x_info:
            roi_info_txt += candi["description"] + " "

    return roi_info_txt.replace("..", ".")


def estimate_frame_rotation(json_result):
    rotation_res = None
    for j_res in json_result["textAnnotations"][1:]:
        try:
            if "Kies" in j_res["description"]:
                if j_res["description"].replace("Kies", "").isdigit():
                    j_res_vertices = j_res["boundingPoly"]["vertices"]
                    if abs(j_res_vertices[0]["y"] - j_res_vertices[1]["y"]) > ROTATION_Y_THREAD:
                        if j_res_vertices[0]["y"] > j_res_vertices[1]["y"]:
                            rotation_res = "clockwise"
                        else:
                            rotation_res = "anti_clockwise"
                    else:
                        if j_res_vertices[0]["x"] > j_res_vertices[1]["x"]:
                            rotation_res = "reflection"
                        else:
                            rotation_res = None
                    break
        except Exception as e:
            print(e)
            log_print(info_str=e)

    return rotation_res


def get_pdf_type(text_info):
    pdf_type = None
    for t_info in text_info["textAnnotations"][1:]:
        for type_key in TYPE.keys():
            if t_info["description"] == "Disposition" and \
                    t_info["boundingPoly"]["vertices"][0]["x"] > \
                    0.5 * text_info["textAnnotations"][0]["boundingPoly"]["vertices"][1]["x"]:
                continue
            if t_info["description"] in TYPE[type_key]:
                pdf_type = type_key
                break
        if pdf_type is not None:
            break

    return pdf_type


def search_specific_info(json_result, search_word):
    spec_info_ret = False
    for j_info in json_result:
        if j_info["description"] in search_word:
            spec_info_ret = True
            break

    return spec_info_ret


if __name__ == '__main__':
    get_pdf_type(text_info={})

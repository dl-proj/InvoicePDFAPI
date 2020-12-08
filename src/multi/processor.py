import ntpath

from src.invoice.extractor import InvoiceExtractor
from utils.folder_file_manager import log_print


class InvoiceMultiProcessor:
    def __init__(self):
        self.invoice_extractor = InvoiceExtractor()
        self.multi_pdf_result = {}

    def main(self, pdf_files):
        self.multi_pdf_result = {}
        for p_file in pdf_files:
            p_file_name = ntpath.basename(p_file).replace(".pdf", "")
            try:
                invoice_result = self.invoice_extractor.run(pdf_path=p_file, pdf_file_name=p_file_name)
                self.multi_pdf_result[ntpath.basename(p_file)] = invoice_result
            except Exception as e:
                log_print(e)

        return self.multi_pdf_result


if __name__ == '__main__':
    InvoiceMultiProcessor().main(pdf_files=[])

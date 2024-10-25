import os
from docx import Document
from pdf2docx import Converter
import uuid


class TextSplit(object):
    def __init__(self):
        pass

    def paragraph_split(self, doc):
        """use doc paragraph split

        Args:
            doc (object): use python-docx load doc file

        Returns:
            list: analyse list
        """
        data_sum = []
        for para in doc.paragraphs:
            if para.text:
                data_sum.append(para.text)
        return data_sum

    def doc_split(self, file_path):

        doc = Document(file_path)

        data_sum = self.paragraph_split(doc)
        return data_sum

    def pdf_split(self, file_path):
        docx_file_name = ""
        try:
            pdf_dir = os.path.dirname(file_path)

            # step1 pdf convert doc
            cv = Converter(file_path)

            docx_file_uuid = f"{uuid.uuid4()}.docx"
            docx_file_name = os.path.join(pdf_dir, docx_file_uuid)

            cv.convert(docx_file_name, start=0, end=None)
            cv.close()
            # step2 doc analyse
            data_sum = self.doc_split(docx_file_name)
            return data_sum

        finally:
            # step3 remove doc file
            if os.path.exists(docx_file_name):
                os.remove(docx_file_name)

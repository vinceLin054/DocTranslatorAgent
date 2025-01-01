# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : pdf_reader.py
# Time       ：2025/1/1 13:13
# Author     ：vince
# Description：
"""
from typing import List

import fitz
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal, LTChar
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pymupdf import Document

from core.models.layout.yolo import YOLOLayout
from core.models.ocr.paddle import PaddleOCR
from core.reader.reader import BaseReader
from core.reader.vo import ReaderResult

class PdfTextReader(BaseReader):

    def read(self) -> List[ReaderResult]:
        result = []
        for page_no, page in enumerate(PDFPage.get_pages(self.file)):
            result.append(ReaderResult(page_no=page_no, text_blocks=self.read_from_page(page_no, page)))
        return result

    def __init__(self, file):
        super().__init__(file)
        resource_manager = PDFResourceManager()
        laparams = LAParams()
        self.device = PDFPageAggregator(resource_manager, laparams=laparams)
        self.page_interpreter = PDFPageInterpreter(resource_manager, self.device)
        self.doc = Document(stream=file.read())
        self.page_count = sum(1 for _ in PDFPage.get_pages(file))
        self.layout_model = YOLOLayout()


    def read_from_page(self, page_no, page):
        doc_page = self.doc.load_page(page_no)
        pix = doc_page.get_pixmap()
        text_blocks = self.layout_model.split_blocks(pix)

        self.page_interpreter.process_page(page)
        layout = self.device.get_result()
        for element in layout:
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text()
                x0, y0, x1, y1 = element.bbox
                x0, y0, x1, y1 = (
                    int(x0),
                    int(y0),
                    int(x1),
                    int(y1)
                )
                for block in text_blocks:
                    if (block.x0 <= x0 and block.six_y0 <= y0 and
                            block.x1 >= x1 and block.six_y1 >= y1):
                        block.text = block.text + text
                        block.font_size = self.get_max_font_size(element)
        return text_blocks

    def get_max_font_size(self, para):
        max_font_size = 0
        for obj in para:
            if isinstance(obj, LTChar):
                max_font_size = obj.size if obj.size > max_font_size else max_font_size
            elif hasattr(obj, '__iter__'):
                for sub_obj in obj:
                    if isinstance(sub_obj, LTChar):
                        max_font_size = sub_obj.size if sub_obj.size > max_font_size else max_font_size
        return max_font_size

class PdfOcrReader(BaseReader):

    def read(self) -> List[ReaderResult]:
        result = []
        for page_no, page in enumerate(PDFPage.get_pages(self.file)):
            result.append(ReaderResult(page_no=page_no, text_blocks=self.read_from_page(page_no, page)))
        return result

    def __init__(self, file):
        super().__init__(file)
        self.doc = Document(stream=file.read())
        self.page_count = sum(1 for _ in PDFPage.get_pages(file))
        self.layout_model = YOLOLayout()
        self.ocr_model = PaddleOCR()

    def read_from_page(self, page_no, page):
        doc_page = self.doc.load_page(page_no)
        pix = doc_page.get_pixmap()
        text_blocks = self.layout_model.split_blocks(pix)

        # 切割小图片做ocr
        for block in text_blocks:
            #
            react = fitz.Rect(block.x0 - 2, block.y0 - 2, block.x1 + 2, block.y1 + 2)
            clip = doc_page.get_pixmap(clip=react)
            text, font_size = self.ocr_model.ocr(clip.tobytes("png"))
            block.text = text
            block.font_size = font_size
        return text_blocks
# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : pdf_ocr_reader_test.py
# Time       ：2025/1/1 15:48
# Author     ：vince
# Description：
"""
from core.reader.pdf_reader import PdfOcrReader

if __name__ == '__main__':
    file_path = 'C:/Users/41593/Downloads/attention is all you need.pdf'  # 替换为你的 PDF 文件路径
    with open(file_path, 'rb') as file:
        res = PdfOcrReader(file).read()
        print(1)
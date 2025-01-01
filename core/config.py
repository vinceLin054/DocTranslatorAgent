# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : config.py
# Time       ：2025/1/1 21:19
# Author     ：vince
# Description：
"""
from core.reader.pdf_reader import PdfTextReader, PdfOcrReader
from core.reader.reader import BaseReader

reader_map: dict = {
    "PdfTextReader": PdfTextReader,
    "PdfOcrReader": PdfOcrReader
}
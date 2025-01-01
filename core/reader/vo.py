# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : vo.py
# Time       ：2025/1/1 14:31
# Author     ：vince
# Description：
"""
from typing import List


class TextBlock:
    def __init__(self, x0, y0, x1, y1, six_y0, six_y1, type):
        self.x0: int = x0
        self.y0: int = y0
        self.six_y0: int = six_y0
        self.x1: int = x1
        self.y1: int = y1
        self.six_y1: int = six_y1
        self.type: str = type
        self.font_size: int = 0
        self.is_bold: bool = 'title' in type or 'caption' in type
        self.text: str = ''

class ReaderResult:
    def __init__(self, page_no: int, text_blocks: List[TextBlock]):
        self.page_n0 = page_no
        self.text_blocks = text_blocks
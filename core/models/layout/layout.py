# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : layout.py
# Time       ：2025/1/1 15:04
# Author     ：vince
# Description：
"""
from abc import abstractmethod
from typing import List

from core.reader.vo import TextBlock


class Layout:

    @abstractmethod
    def split_blocks(self, pix) -> List[TextBlock]:
        pass
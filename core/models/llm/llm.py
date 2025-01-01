# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : llm.py
# Time       ：2025/1/1 18:52
# Author     ：vince
# Description：
"""
from abc import abstractmethod


class BaseLlm:

    @abstractmethod
    def predict(self, text):
        pass


    def instance_prompt(self, text, target_lang):
        return [
            {
                "role": "system",
                "content": "You are a professional,authentic machine translation engine.",
            },
            {
                "role": "user",
                "content": f"Translate the following markdown source text to {target_lang}. Keep formulas and subscripts unchanged. Output translation directly without any additional text.\nSource Text: {text}\nTranslated Text:",
            },
        ]
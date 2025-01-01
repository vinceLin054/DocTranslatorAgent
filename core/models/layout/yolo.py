# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : yolo.py
# Time       ：2025/1/1 14:55
# Author     ：vince
# Description：
"""
from typing import List

import numpy as np

from doclayout_yolo import YOLOv10
from huggingface_hub import hf_hub_download

from core.models.layout.layout import Layout
from core.reader.vo import TextBlock

filepath = hf_hub_download(repo_id="juliozhao/DocLayout-YOLO-DocStructBench", filename="doclayout_yolo_docstructbench_imgsz1024.pt")
model = YOLOv10(filepath)

class YOLOLayout(Layout):

    def split_blocks(self, pix) -> List[TextBlock]:
        text_blocks = []
        image = np.fromstring(pix.samples, np.uint8).reshape(
            pix.height, pix.width, 3
        )[:, :, ::-1]
        image_box = np.ones((pix.height, pix.width))
        h, w = image_box.shape
        det_res = model.predict(image, conf=0.6, imgsz=int(pix.height / 32) * 32)[0]
        abandon_block = ["abandon", "figure", "table", "isolate_formula", "formula_caption"]
        for i, box in enumerate(det_res.boxes):
            x0, y0, x1, y1 = box.xyxy.squeeze()
            x0, six_y0, x1, six_y1 = (
                np.clip(int(x0 - 1), 0, w - 1),
                np.clip(int(h - y1 - 1), 0, h - 1),
                np.clip(int(x1 + 1), 0, w - 1),
                np.clip(int(h - y0 + 1), 0, h - 1),
            )
            type = det_res.names[int(box.cls)]
            if type not in abandon_block:
                block = TextBlock(x0=x0, y0=int(y0 - 1), x1=x1, y1=int(y1 + 1), six_y0=six_y0, six_y1=six_y1,
                                  type=type, is_bold='title' in type or 'caption' in type)
                text_blocks.append(block)
        return text_blocks
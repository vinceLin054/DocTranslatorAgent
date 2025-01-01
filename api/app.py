# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : app.py
# Time       ：2025/1/1 21:13
# Author     ：vince
# Description：
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core.config import reader_map


app = FastAPI()

# 设置允许的文件扩展名
ALLOWED_EXTENSIONS = {'pdf'}

# 检查文件是否被允许上传
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post('/get_text_block')
def get_text_block(
    file: UploadFile = File(...),
    reader_name: str = Form(...)
):
    # 检查文件是否是允许的类型
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type is not allowed")

    # 检查文件是否是允许的类型
    if file:
        res = reader_map.get(reader_name)(file.file).read()
        return JSONResponse(content=jsonable_encoder(res))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
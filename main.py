from fastapi import FastAPI, File, UploadFile
from tempfile import NamedTemporaryFile
from typing import List
import os
from fastapi.responses import FileResponse
import cv2
import uvicorn
from paddleocr import PaddleOCR, draw_ocr
from get_head import head
from get_info import ocrr
from Util import response_code
import base64
import cv2

app = FastAPI()

ocrx = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

@app.post("/IDCard2info_front/",summary='上传身份证正面')
async def upload_file(file: UploadFile = File(...)):
    """
    idcard2info
    :param file: file: [filelike]
    :return: information on the front of the IDCard
    {
        “code”: 200
        "message": "Success"
        "data": "the information on the front of the IDCard"
    }
    """
    contents = await file.read()  # 读取数据
    file_copy = NamedTemporaryFile(delete=False)  # 设置临时文件，用于后续读取
    try:
        file_copy.write(contents)  # 把数据写入临时文件
        img = cv2.imread(file_copy.name)
        pic_info= ocrr.get_info(img,ocrx)
        if not pic_info:
            return response_code.resp_400(message="图片上传错误，请上传身份证正面")

        pic_head_base64 = head.tranposeDector(img)  # base64 of the head.jpg
        
    finally:
        file_copy.close()  # to close any file instances before removing the temp file
        os.unlink(file_copy.name)  # unlink (remove) the file


    if not pic_head_base64:
        pic_info["头像"] = "头像解析失败"
        return response_code.resp_200(data=pic_info)
    else:
        pic_info["头像"] = pic_head_base64.decode('utf-8')
        return response_code.resp_200(data=pic_info)

@app.post("/IDCard2info_back/",summary='上传身份证反面')
async def upload_file(file: UploadFile = File(...)):
    """
    idcard2info
    :param file: file: [filelike]
    :return: information on the back of the IDCard
    {
        “code”: 200
        "message": "Success"
        "data": "the information on the back of the IDCard"
    }
    """
    contents = await file.read()  # 读取数据
    file_copy = NamedTemporaryFile(delete=False)  # 设置临时文件，用于后续读取
    try:
        file_copy.write(contents)  # 把数据写入临时文件
        img = cv2.imread(file_copy.name)
        
        pic_info_back= ocrr.get_info_back(img,ocrx)
    finally:
        file_copy.close()  # to close any file instances before removing the temp file
        os.unlink(file_copy.name)  # unlink (remove) the file
    if not pic_info_back:
        return response_code.resp_400(message="图片上传错误，请上传身份证反面")
    else:
        return response_code.resp_200(data=pic_info_back)



@app.post('/IDCard2info/',summary='上传身份证正反')
async def upload_files(files:List[UploadFile]=File(...)):
    '''
    上传身份证正面及反面照片，顺序为：1、正 2、反
    :param file: files:[filelike]
    :return: information of the IDCard
    {
        "code": 200
        "message": "Success"
        "data": "the information of the IDCard"
    }
    '''
    idcard_front = files[0]
    idcard_back = files[1]

    contents_back = await idcard_back.read()
    file_copy_back = NamedTemporaryFile(delete=False)  # 设置临时文件，用于后续读取
    try:
        file_copy_back.write(contents_back)  # 把数据写入临时文件
        img = cv2.imread(file_copy_back.name)
        pic_info_back= ocrr.get_info_back(img,ocrx)
    finally:
        file_copy_back.close()  # to close any file instances before removing the temp file
        os.unlink(file_copy_back.name)  # unlink (remove) the file

    if not pic_info_back:
        return response_code.resp_400(message="图片上传错误，请按正反顺序上传身份证")

    contents_front = await idcard_front.read()  # 读取数据
    file_copy = NamedTemporaryFile(delete=False)  # 设置临时文件，用于后续读取
    try:
        file_copy.write(contents_front)  # 把数据写入临时文件
        img = cv2.imread(file_copy.name)
        pic_head_base64 = head.tranposeDector(img)  # 调用函数(传入文件名)
        pic_info= ocrr.get_info(img,ocrx)
        
    finally:
        file_copy.close()  # to close any file instances before removing the temp file
        os.unlink(file_copy.name)  # unlink (remove) the file
    
    if not pic_info:
        return response_code.resp_400(message="图片上传错误，请按正反顺序上传身份证")
    elif not pic_head_base64:
        
        pic_info.update(pic_info_back)
        pic_info["头像"] = "头像解析失败"
        return response_code.resp_200(data=pic_info)
    else:
        
        pic_info.update(pic_info_back)
        pic_info["头像"] = pic_head_base64.decode('utf-8')
        return response_code.resp_200(data=pic_info)


    return pic_info


@app.post("/IDCard2Pic/",summary='头像信息')
async def upload_file(file: UploadFile = File(...)):

    contents = await file.read()  # 读取数据
    file_copy = NamedTemporaryFile(delete=False)  # 设置临时文件，用于后续读取
    try:
        file_copy.write(contents)  # 把数据写入临时文件
        img = cv2.imread(file_copy.name)
        pic_head = head.tranposeDector2(img)  # np of the head_pic
        
    finally:
        file_copy.close()  # to close any file instances before removing the temp file
        os.unlink(file_copy.name)  # unlink (remove) the file


    if pic_head is False:
        return response_code.resp_400(data="头像解析失败")
    else:
        try:
            file_copy1 = NamedTemporaryFile(delete=False, dir='./temp_pic', suffix='.jpg')
            cv2.imwrite(file_copy1.name, pic_head)
            return FileResponse(file_copy1.name)
            
        finally:
            file_copy1.close()
            
        

    
    

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True, debug=True)

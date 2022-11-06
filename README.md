# 基于PaddleOCR OpenCV FastApi的 身份证信息识别 和 身份证头像提取 工具

# Docker使用

## 文件描述
1. gunicorn.config.py:
    - gunicorn配置文件，可更改进程数，默认5。
在构建镜像前更改可生效。
2. Dockerfile:
    - Docker镜像的描述文件。

## 使用流程

### 自行构建镜像(有更改进程数等需求)
```shell
#构建镜像
docker build -t fastapi_ocr:1.2 .

#创建容器
docker run -d --name IDCard_OCR -p 8000:8000 fastapi_ocr:1.2
```

### 使用现有镜像(镜像有点大，如果需要可以在Issues中提)
```shell
#load镜像
docker load -i images.tar

#创建容器
docker run -d --name IDCard_OCR -p 8000:8000 fastapi_ocr:1.2
```
### api文档地址
```
http://ip:8000/docs
```


# 本机安装

## 1.安装依赖（Python 3.7）
### 1.1 安装PaddlePaddle
`python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple`
### 1.2 安装requirements.txt
`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 2. 启动服务
```shell
#port:9999
nohup gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9999 &
```

## 3. 接口列表
### 3.1 http://IP:9999/IDCard2info_front/
the information on the front of the IDCard
#### 3.1.1 请求参数（post）
- file: [身份证正面图片]
#### 3.1.2 返回参数
- { "code": 200 "message": "Success" "data": "the information on the front of the IDCard" }
  - "data"：
    - 身份证正面信息
    - base64 of 头像.jpg
- { "code": 400 "message": "Error message" "data": "null" }
    - "message":
      - 图片上传错误 

### 3.2 http://IP:9999/IDCard2info_back/
the information on the back of the IDCard
#### 3.2.1 请求参数（post）
- file: [身份证背面图片]
#### 3.2.2 返回参数
- { "code": 200 "message": "Success" "data": "the information on the back of the IDCard" }
- "data"：
    - 身份证背面信息
- { "code": 400 "message": "Error message" "data": "null" }
    - "message":
      - 图片上传错误 

### 3.3 http://IP:9999/IDCard2info/
the information of the IDCard
#### 3.3.1 请求参数（post）
- files: [身份证正面图片,身份证反面图片]
#### 3.3.2 返回参数
- { "code": 200 "message": "Success" "data": "the information of the IDCard" }
- "data"：
    - 身份证正面信息
    - 身份证反面信息
    - base64 of 头像.jpg
- { "code": 400 "message": "Error message" "data": "null" }
    - "message":
      - 图片上传错误 

## 4. TODO
- 增加ocr大模型的api接口，提高精准度但会降低识别效率。

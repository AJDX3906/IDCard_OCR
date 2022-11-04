FROM python:3.7
RUN sed -i "s@http://\(deb\|security\).debian.org@https://mirrors.tencent.com@g" /etc/apt/sources.list
RUN apt-get update -y --fix-missing && apt-get upgrade -y
RUN apt-get install cmake ffmpeg libsm6 libxext6  -y
WORKDIR /code
COPY . .
COPY /paddleocr /root/.paddleocr
RUN pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple
RUN pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/web/simple
EXPOSE 8000
CMD ["gunicorn", "main:app", "-c", "./gunicorn.config.py"]

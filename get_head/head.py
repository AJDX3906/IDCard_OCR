#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cv2
import dlib
import numpy as np
import os, sys, time
from random import randint

import base64



def tranposeDector(img, cnt=0):
    # 返回base64 of jpg
    '''
    :param infile:  imread后的图片对象
    '''
    # 检测图上的人脸数
    dector = dlib.get_frontal_face_detector()
    try:
        dets = dector(img, 1)
    except Exception as ex:  # 脸部无法检测
        return False
    # 身份证上只能有一个人脸，即为检查结果的第一个值
    if dets:
        face = dets[0]  # [(354, 96) (444, 186)] 检测出左上、右下两个点
        # 计算想裁取的图片的高度 下-上
        height = face.bottom() - face.top() + 85
        # 计算想裁取的图片的宽度 右-左
        width = face.right() - face.left() + 45
        # 以计算出的图片大小生成空白板
        img_blank = np.zeros((height, width, 3), np.uint8)
        # 将图片写入空白板
        try:
            for i in range(height):
                for j in range(width):  # top线上方40像素位置开始读, left线左15像素位置开始读
                    img_blank[i][j] = img[face.top() - 40 + i][face.left() - 15 + j]
            base64_str = cv2.imencode('.jpg',img_blank)[1].tostring()
            base64_str = base64.b64encode(base64_str)
            cv2.destroyAllWindows()  # 释放所有窗口资源

            return base64_str
        except Exception as ex:
            return False

        cv2.destroyAllWindows()  # 释放所有窗口资源
    else:
        cnt += 1
        if cnt < 3:
            transposeImage = cv2.transpose(img)  # 图像反向旋转90度
            flipedImageX = cv2.flip(transposeImage, 0)  # 沿X轴方向的镜像图片
            cv2.imshow("flipedImageX",flipedImageX)
            cv2.waitKey(1000)
            tranposeDector(flipedImageX, cnt)
        else:
            print("人脸检测失败 transpose times:", cnt)
            cv2.destroyAllWindows()  # 释放所有窗口资源
            return False

def tranposeDector2(img, cnt=0):
    # 返回图片
    '''
    :param infile:  imread后的图片对象
    '''
    # 检测图上的人脸数
    dector = dlib.get_frontal_face_detector()
    try:
        dets = dector(img, 1)
    except Exception as ex:  # 脸部无法检测
        return False
    # 身份证上只能有一个人脸，即为检查结果的第一个值
    if dets:
        face = dets[0]  # [(354, 96) (444, 186)] 检测出左上、右下两个点
        # 计算想裁取的图片的高度 下-上
        height = face.bottom() - face.top() + 85
        # 计算想裁取的图片的宽度 右-左
        width = face.right() - face.left() + 45
        # 以计算出的图片大小生成空白板
        img_blank = np.zeros((height, width, 3), np.uint8)
        # 将图片写入空白板
        try:
            for i in range(height):
                for j in range(width):  # top线上方40像素位置开始读, left线左15像素位置开始读
                    img_blank[i][j] = img[face.top() - 40 + i][face.left() - 15 + j]
            
            
            
            cv2.destroyAllWindows()  # 释放所有窗口资源

            return img_blank
        except Exception as ex:
            return False

        cv2.destroyAllWindows()  # 释放所有窗口资源
    else:
        cnt += 1
        if cnt < 3:
            transposeImage = cv2.transpose(img)  # 图像反向旋转90度
            flipedImageX = cv2.flip(transposeImage, 0)  # 沿X轴方向的镜像图片
            cv2.imshow("flipedImageX",flipedImageX)
            cv2.waitKey(1000)
            tranposeDector(flipedImageX, cnt)
        else:
            print("人脸检测失败 transpose times:", cnt)
            cv2.destroyAllWindows()  # 释放所有窗口资源
            return False

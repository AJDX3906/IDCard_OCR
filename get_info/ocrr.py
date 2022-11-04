from paddleocr import PaddleOCR

def get_info(img_path,ocrx):
    #ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    result = ocrx.ocr(img_path, cls=True)
    info = []
    for line in result:
        info.append(line[1][0])
    
    info_length = len(info)
    if info_length < 8 or info_length > 11:
        return False
    if(len(info[info_length-1])!=18):
        return False
    final_info = {}
    final_info["姓名"] = info[0][2:]
    final_info["性别"] = info[1][2:3]
    final_info["民族"] = info[1][5:]
    final_info["出生"] = info[3]

    address = ""
    for i in range(info_length - 7):
        address = address + info[5+i]
    final_info["住址"] = address

    final_info["公民身份证号码"] = info[info_length-1]
    

    return final_info


def get_info_back(img_path,ocrx):
    #ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    result = ocrx.ocr(img_path, cls=True)
    info = []
    for line in result:
        info.append(line[1][0])
    if len(info) != 6:
        return False
    final_info = {}
    final_info["签发机关"] = info[3]
    final_info["有效期限"] = info[5]

    return final_info

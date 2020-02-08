# -*- coding: utf-8 -*-

import os
import argparse
import cv2
import numpy as np
from PIL import Image
import pyocr
import pyocr.builders

def getFileName(path):
    name = os.path.splitext(os.path.basename(path))[0]
    return name

def ocr(filePath, tool, language, layout):
    result = tool.image_to_string(
        Image.open(filePath),
        lang=language,
        builder=pyocr.builders.TextBuilder(tesseract_layout=layout))
    return result


# def convertAndSaveImage(filepath, filename, H, S, V):
def convertAndSaveImage(filepath, filename, threshold):
    try:
        outputfilepath = './' + getFileName(filepath) + "_" + str(threshold) +"_filter2D.png"

        # outputfilepath = './' + getFileName(filepath)+ "_" + str(H) + "_" + str(S) + "_" + str(V) + ".png"
        # img = cv2.imread(filepath)
        # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # #マスクの作成
        # lower_black = np.array([0,0,0])
        # upper_black = np.array([H,S,V])
        # # 黒文字の抽出
        # mask = cv2.inRange(hsv, lower_black, upper_black)
        # # 反転
        # res = cv2.bitwise_not(mask)
        # # ノイズ除去
        # res2 = cv2.fastNlMeansDenoising(res)
        # cv2.imwrite(outputfilepath, res2)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float32)

        img = cv2.imread(filepath, 0)
        dst  = cv2.fastNlMeansDenoising(img)
        ret, dst2 = cv2.threshold(dst, threshold, 255, cv2.THRESH_BINARY)
        img_thresh = cv2.filter2D(dst2, -1, kernel)
        cv2.imwrite(outputfilepath, img_thresh)

        # img = cv2.imread(filepath,0)
        # ret2, img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
        # #閾値がいくつになったか確認
        # print("ret2: {}".format(ret2))
        # cv2.imwrite(outputfilepath, img_otsu)

        return outputfilepath
    except Exception as e:
        raise Exception("Internal error at convertAndSaveImage: "+ str(e))


if __name__ == '__main__':
    # constant
    layout_num = 6

    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, default="debug")
    args = parser.parse_args()

    if (args.mode != "debug" and args.mode != "ci"):
        exit(0)

    if args.mode == "debug":
        print("=== Debug Mode ===")

    image_dir = "../images" if args.mode == "debug" else "data/test"

    files = [
        filename for filename in os.listdir(image_dir)
        if os.path.splitext(filename)[-1].lower() in ['.jpg', '.png']
    ]

    # get tesseract-ocr
    tools = pyocr.get_available_tools()
    tool = tools[0]

    for filename in files:
        filepath = image_dir + "/" + filename
        img = cv2.imread(filepath,0)
        ret, img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
        
        for th in range(int(ret)-9, int(ret)+22, 3):
            tmpImgPath = convertAndSaveImage(filepath, filename, th)
            ocr_result = ocr(tmpImgPath, tool, "eng+jpn", layout_num)
            imageOutName = './' + getFileName(filepath) + "_" + str(th) + '_filter2D.txt'
            with open(imageOutName, 'w') as f:
                f.write(ocr_result)

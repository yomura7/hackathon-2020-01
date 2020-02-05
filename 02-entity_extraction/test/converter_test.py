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


def convertAndSaveImage(filepath, filename, H, S, V):
    try:
        outputfilepath = './' + getFileName(filepath)+ "_" + str(H) + "_" + str(S) + "_" + str(V) + ".png"
        img = cv2.imread(filepath)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #マスクの作成
        lower_black = np.array([0,0,0])
        upper_black = np.array([H,S,V])
        # 黒文字の抽出
        mask = cv2.inRange(hsv, lower_black, upper_black)
        # 反転
        res = cv2.bitwise_not(mask)
        # ノイズ除去
        res2 = cv2.fastNlMeansDenoising(res)
        cv2.imwrite(outputfilepath, res2)
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
        #Loop HSV
        for H in range(0, 370, 10):
            for S in range(0, 110, 10):
                for V in range(80, 105, 5):
                    tmpImgPath = convertAndSaveImage(filepath, filename, H, S, V)
                    # ocr_result = ocr(tmpImgPath, tool, "eng+jpn", layout_num)
                    # imageOutName = './' + getFileName(filepath) + "_" + str(H) + "_" + str(S) + "_" + str(V) + '.txt'
                    # with open(imageOutName, 'w') as f:
                    #     f.write(ocr_result)

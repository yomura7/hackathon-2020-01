from PIL import Image
import pyocr
import pyocr.builders
import glob
import csv

def ocr(filePath):
    for imagePath in glob.glob(filePath):
        result = tool.image_to_string(
            Image.open(imagePath),
            lang=LANGUAGE,
            builder=pyocr.builders.TextBuilder(tesseract_layout=LAYOUT_NUM))
    return result

def parser(str):
    return [0,1,2,3,4]


LANGUAGE = "eng+jpn"
LAYOUT_NUM = 6
tools = pyocr.get_available_tools()
tool = tools[0]
srcPath = "./images/*.png"
outPath = "./result.csv"

with open(outPath, 'w') as f:
    writer = csv.writer(f)
    for imagePath in glob.glob(srcPath):
        ocrResult = ocr(imagePath)
        result = parser(ocrResult)
        writer.writerow(result)


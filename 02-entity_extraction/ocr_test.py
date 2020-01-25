from PIL import Image
import pyocr
import pyocr.builders
import glob
import csv
import os
import sqlite3
import pandas

def getFileName(path):
    name = os.path.splitext(os.path.basename(path))[0]
    return name

def getFileNameWithExt(path):
    name = os.path.basename(path)
    return name

def ocr(filePath, language):
    result = tool.image_to_string(
        Image.open(filePath),
        lang=language,
        builder=pyocr.builders.TextBuilder(tesseract_layout=LAYOUT_NUM))
    imageOutName = './tmp/' + getFileName(filePath) + '.txt'
    with open(imageOutName, 'w') as f:
        f.write(result)
    return result

#filename,origin,destination,line,company,price,issued_on,available_from,expire_on
def parser(filename, str):
    return [filename,1,2,3,4]






DB_PATH = './resource/train.db'
LAYOUT_NUM = 6
tools = pyocr.get_available_tools()
tool = tools[0] # tesseract
srcPath = "./images/*.png"
outPath = "./tmp/result.csv"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

with open(outPath, 'w') as f:
    writer = csv.writer(f)
    for imagePath in glob.glob(srcPath):
        name = getFileNameWithExt(imagePath)
        ocrResult = ocr(imagePath, "eng+jpn")
        # ocrResult = ocr(imagePath, "jpn+eng")
        result = parser(name, ocrResult)
        writer.writerow(result)

# word = '_府'
# for row in cur.execute('SELECT * FROM station WHERE station_name like ?', (word,)):
#     print(row)

cur.close()
conn.close()
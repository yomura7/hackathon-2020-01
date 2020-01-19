from PIL import Image
import pyocr
import pyocr.builders
import glob
import csv
import os
import sqlite3
import pandas
import re
import regex
import io
import unicodedata
import datetime

def getFileName(path):
    name = os.path.splitext(os.path.basename(path))[0]
    return name

def getFileNameWithExt(path):
    name = os.path.basename(path)
    return name

def ocr(filePath):
    result = tool.image_to_string(
        Image.open(filePath),
        lang=LANGUAGE,
        builder=pyocr.builders.TextBuilder(tesseract_layout=LAYOUT_NUM))
    imageOutName = './tmp/' + getFileName(filePath) + '.txt'
    with open(imageOutName, 'w') as f:
        f.write(result)
    return result

#filename,origin,destination,line,company,price,issued_on,available_from,expire_on
def parser(filename, text):
    station_list = []
    comapny_list = []
    line_list = []
    price_list = []
    date_list = []
    buf = io.StringIO(text)
    line = buf.readline()
    while line:
        s = unicodedata.normalize("NFKC",line.strip().replace(" ", ""))
        #料金を含んでいるかチェック
        price = findPrice(s)
        if price is not None:  price_list.append(price) 
        #日付を含んでいるかチェック
        date = findDate(s)
        if date is not None: date_list.append(date)
        #単語を含んでいるかチェック
        words = wordBlockRegex.findall(s)
        #単語ごとに該当の駅、会社、路線がチェック
        for word in words:
            #駅名を含んでいるかチェック
            station = findStation(word)
            if station is not None: station_list.append(station)
            #会社名を含んでいるかチェック
            company = findCompany(word)
            if company is not None: comapny_list.append(company)
            #路線名を含んでいるかチェック
            line = findLine(word)
            if line is not None: line_list = line              
        line = buf.readline()
    filename = filename if filename is not None else ""
    origin = station_list[0] if len(station_list) > 0 else ""
    dest = station_list[1] if len(station_list) > 1 else ""
    line = line_list[0] if len(line_list) > 0 else ""
    company = comapny_list[0] if len(comapny_list) > 0 else ""
    price = price_list[0] if len(price_list) > 0 else 0
    issued_on = date_list[0] if len(date_list) > 0 else ""
    return [filename,origin,dest,line,company,price,issued_on,issued_on,issued_on]

#初めにマッチしたものを返す　可能性の高い駅順に並べる必要あるかも
def findStation(word):
    for row in cur.execute('SELECT station_name FROM station WHERE station_name like ?', (word,)):
        return row[0]

def findCompany(word):
    #初めにマッチしたものを返す　可能性の高い会社順に並べる必要あるかも
    for row in cur.execute('SELECT company_name FROM company WHERE company_name like ?', (word,)):
        return row[0]

def findLine(word):
    #初めにマッチしたものを返す　可能性の高い路線順に並べる必要あるかも
    for row in cur.execute('SELECT line_name FROM line WHERE line_name like ?', (word,)):
        return row[0]

def findPrice(line):
    prices = priceRegex.findall(line)
    #円￥¥以外の表記に対応するためには以下を修正する
    if len(prices) is not 0: return re.sub(r'[円￥¥,]', "", prices[0])

def findDate(line):
    dates = dateRegex.findall(line)
    if len(dates) is 0:
        return
    #最初にマッチした要素を結果にする。修正する必要あるかも
    date = dates[0]
    if re.match(r'[0-9]{2}\.-', date) is not None:
        date = convertFromOmittedDate(date)
    if re.match(r'[0-9]{4}\.-', date) is not None:
        date = re.sub(r'\.-', '-', date)
    #年月日、-以外の表記に対応するためには以下を修正する
    return date.replace("年","-").replace("月","-").replace("日","").replace(".","-")

#19.-12.21のような省略系の日付を変換する。和暦非対応。
#2019なのか1919なのか分からないので2000年に倒す
def convertFromOmittedDate(date):
    num = int(re.sub(r'\.-.*', '', date))
    head = None
    if (thisyear % 100) > num:
        head = str(int(thisyear / 100)) + str(num)
    else:
        head = '19' + str(num)
    result = head + re.sub(r'.*\.-', '-', date).replace('.','-')
    return result

def debugSQL(table, column, word):
    for row in cur.execute('SELECT ' + column + ' FROM ' + table + ' WHERE ' + column + ' like ?', (word,)):
        print(row)

DB_PATH = './resource/train.db'
LANGUAGE = "eng+jpn"
LAYOUT_NUM = 6
tools = pyocr.get_available_tools()
tool = tools[0]
srcPath = "./images/*.png"
outPath = "./tmp/result.csv"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
wordBlockRegex = regex.compile(r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}]+')
dateRegex = regex.compile('(?:(?:[1-9]|1[0-2])月(?:[1-9]|[12][0-9]|3[01])日)|(?:(?:19[0-9]{2}|20[0-9]{2}|[0-9]{2})\.?-(?:[1-9]|1[0-2])(?:\.|-)(?:3[0-1]|[1-2][0-9]|[1-9]))')
priceRegex = regex.compile('(?:[1-9][0-9]{2,4}円)|(?:[￥¥][1-9][0-9]{2,4})|(?:[1-9],[0-9]{3,4}円)|(?:[￥¥][1-9],[0-9]{3,4})')
thisyear = datetime.date.today().year

with open(outPath, 'w') as f:
    writer = csv.writer(f)
    for imagePath in glob.glob(srcPath):
        name = getFileNameWithExt(imagePath)
        # preprocess
        ocrResult = ocr(imagePath)
        result = parser(name, ocrResult)
        writer.writerow(result)

cur.close()
conn.close()
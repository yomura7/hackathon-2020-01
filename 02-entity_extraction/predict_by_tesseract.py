# -*- coding: utf-8 -*-

import os
import sys
import csv
import argparse
import sqlite3
import re
import io
import unicodedata
import datetime
import regex
import cv2
import numpy as np
from PIL import Image
import pyocr
import pyocr.builders

def getFileName(path):
    name = os.path.splitext(os.path.basename(path))[0]
    return name


def getFileNameWithExt(path):
    name = os.path.basename(path)
    return name


def ocr(filePath, tool, language, layout):
    result = tool.image_to_string(
        Image.open(filePath),
        lang=language,
        builder=pyocr.builders.TextBuilder(tesseract_layout=layout))
    imageOutName = './tmp/' + getFileName(filePath) + '.txt'
    with open(imageOutName, 'w') as f:
        f.write(result)
    return result


# filename,origin,destination,line,company,price,issued_on,available_from,expire_on
def parse(filename, text):
    wordBlockRegex = regex.compile(r'[\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Han}]+')
    station_list = []
    comapny_list = []
    line_list = []
    price_list = []
    date_list = []
    buf = io.StringIO(text)
    line = buf.readline()
    while line:
        s = unicodedata.normalize("NFKC",line.strip().replace(" ", ""))
        # 料金を含んでいるかチェック
        price = findPrice(s)
        if price is not None:  price_list.append(price)
        # 日付を含んでいるかチェック
        date = findDate(s)
        if date is not None: date_list.append(date)
        # 単語を含んでいるかチェック
        words = wordBlockRegex.findall(s)
        # 単語ごとに該当の駅、会社、路線がチェック
        for word in words:
            # 駅名を含んでいるかチェック
            station = findStation(word)
            if station is not None: station_list.append(station)
            # 会社名を含んでいるかチェック
            company = findCompany(word)
            if company is not None: comapny_list.append(company)
            # 路線名を含んでいるかチェック
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


def findStation(word):
    #TODO 初めにマッチしたものを返す　可能性の高い駅順に並べる必要あるかも
    for row in cur.execute('SELECT station_name FROM station WHERE station_name like ?', (word,)):
        return row[0]


def findCompany(word):
    #TODO 初めにマッチしたものを返す　可能性の高い会社順に並べる必要あるかも
    for row in cur.execute('SELECT company_name FROM company WHERE company_name like ?', (word,)):
        return row[0]


def findLine(word):
    #TODO 初めにマッチしたものを返す　可能性の高い路線順に並べる必要あるかも
    for row in cur.execute('SELECT line_name FROM line WHERE line_name like ?', (word,)):
        return row[0]


def findPrice(line):
    priceRegex = regex.compile('(?:[1-9][0-9]{2,4}円)|(?:[￥¥][1-9][0-9]{2,4})|(?:[1-9],[0-9]{3,4}円)|(?:[￥¥][1-9],[0-9]{3,4})')
    prices = priceRegex.findall(line)
    # 円￥¥以外の表記に対応するためには以下を修正する
    if len(prices) is not 0: return re.sub(r'[円￥¥,]', "", prices[0])


def findDate(line):
    try:
        #TODO: 年が存在しない場合など、断片的にOCRできる場合に予測できるように変更する必要があるかも
        #TODO: リファクタリング　冗長なのでつなぎ文字をorにして短くする
        dateRegex = regex.compile('(?:(?:19[0-9]{2}|20[0-9]{2}|[0-9]{2})年(?:[1-9]|1[0-2])月(?:[1-9]|[12][0-9]|3[01])日)|(?:(?:19[0-9]{2}|20[0-9]{2}|[0-9]{2})\.?-(?:[1-9]|1[0-2])(?:\.|-)(?:3[0-1]|[1-2][0-9]|[1-9]))')
        dates = dateRegex.findall(line)
        if len(dates) is 0:
            return
        #TODO: 最初にマッチした要素を結果にする。修正する必要あるかも
        date = dates[0]
        if re.match(r'[0-9]{2}\.-', date) is not None:
            date = convertFromOmittedDate(date)
        if re.match(r'[0-9]{4}\.-', date) is not None:
            date = re.sub(r'\.-', '-', date)
        date = date.replace("年", "-").replace("月", "-").replace("日", "").replace(".", "-")
        #パディング処理
        date = zeroPadding(date)
        return date
    except:
        #raise ValueError("Failed to find date in " + line + ", Detail: " + str(e))
        return ""


def zeroPadding(date):
    try:
        year = int(re.sub(r'-.*', '', date))
        month = int(re.sub(r'.*-(.*)-.*', r'\1', date))
        day = int(re.sub(r'.*-.*-', '', date))
        return datetime.date(year, month, day).strftime('%Y-%m-%d')
    except:
        #raise ValueError("Failed to padding date:" + date)
        return ""


# 19.-12.21のような省略系の日付を変換する。和暦非対応。
# 2019なのか1919なのか分からないので2000年に倒す
def convertFromOmittedDate(date):
    num = int(re.sub(r'\.-.*', '', date))
    thisyear = datetime.date.today().year
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


def print_to_stdout(files):
    writer = csv.writer(sys.stdout)
    for filename in files:
        origin = ""
        destination = ""
        line = ""
        company = ""
        price = ""
        issued_on = ""
        available_from = ""
        expire_on = ""
        writer.writerow([
            filename, origin, destination, line, company,
            price, issued_on, available_from, expire_on])


def convertAndSaveImage(filepath, filename):
    outputfilepath = "./tmp/" + filename
    img = cv2.imread(filepath, 0)
    # ノイズ除去
    dst = cv2.fastNlMeansDenoising(img)
    # ヒストグラム平坦化　←微妙
    # equ = cv2.equalizeHist(dst)
    #閾値処理
    #thresh2 = cv2.fastNlMeansDenoising(dst2))　←2回目掛けるとかすれる。
    ret, dst2 = cv2.threshold(dst, 160, 255, cv2.THRESH_BINARY)
    cv2.imwrite(outputfilepath, dst2)
    return outputfilepath


if __name__ == '__main__':
    # constant
    db_path = './resource/train.db'
    layout_num = 6

    parser = argparse.ArgumentParser()
    # parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    parser.add_argument('--mode', type=str, default="debug")
    args = parser.parse_args()

    if (args.mode != "debug" and args.mode != "ci"):
        exit(0)

    if args.mode == "debug":
        print("=== Debug Mode ===")

    image_dir = "images" if args.mode == "debug" else "data/test"
    output_path = "tmp/result.csv" if args.mode == "debug" else sys.stdout

    files = [
        filename for filename in os.listdir(image_dir)
        if os.path.splitext(filename)[-1].lower() in ['.jpg', '.png']
    ]

    # get tesseract-ocr
    tools = pyocr.get_available_tools()
    tool = tools[0]

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    if args.mode == "debug":
        writer = csv.writer(open(output_path, 'w'))
    else:
        writer = csv.writer(sys.stdout)

    for filename in files:
        filepath = image_dir + "/" + filename
        tmpImgPath = convertAndSaveImage(filepath, filename)
        ocr_result = ocr(tmpImgPath, tool, "eng+jpn", layout_num)
        result = parse(filename, ocr_result)

        # debug
        if args.mode == "debug":
            print(result)

        writer.writerow(result)

    cur.close()
    conn.close()

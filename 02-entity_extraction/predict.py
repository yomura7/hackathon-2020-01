import os
import sys
import csv
import argparse
import pyocr
import pyocr.builders

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str)
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    files = [
        filename for filename in os.listdir(args.image_dir)
        if os.path.splitext(filename)[-1].lower() in ['.jpg', '.png']
    ]

    # Check available OCR tools
    tools = pyocr.get_available_tools()
    tesseract = tools[0]

    writer = csv.writer(args.output)
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

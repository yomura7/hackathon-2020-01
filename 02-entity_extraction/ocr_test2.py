import pyocr
import pyocr.builders
import cv2
from PIL import Image 
import sys

imagePath = "./images/sample5.png"

tools = pyocr.get_available_tools()

if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

tool = tools[0]

res = tool.image_to_string(Image.open(imagePath),
                           lang="eng+jpn",
                           builder=pyocr.builders.WordBoxBuilder(tesseract_layout=6))

out = cv2.imread(imagePath)
for d in res:
    print(d.content)
    # print(d.position)
    cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2)

cv2.imshow("img",out)
cv2.waitKey(0)
cv2.destroyAllWindows()
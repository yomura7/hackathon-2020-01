from PIL import Image
import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
tool = tools[0]
result = tool.image_to_string(
    Image.open(".images/sample1.png"),
    lang="jpn", builder=pyocr.builders.TextBuilder(tesseract_leyout=6))

with open('images/sample1.txt', 'w') as f:
    f.write(result)

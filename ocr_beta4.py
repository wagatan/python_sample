# ocrbeta.py
import os
from PIL import Image, ImageOps
import pyocr
import pyocr.builders
import cv2


# 1.インストール済みのTesseractのパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# 2.OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]

# pyocrへ利用するOCRエンジンをTesseractに指定する。
tools = pyocr.get_available_tools()
tool = tools[0]
 
#OCR対象の画像ファイルを読み込む
img = Image.open("./img/fpv.jpg")
path= "./result/out.jpg"
img.save(path)

#画像を読みやすいように加工。
img=img.convert('RGB')
size=img.size

img2=Image.new('RGB',size)
border=110
 
for x in range(size[0]):
    for y in range(size[1]):
        r,g,b=img.getpixel((x,y))
        if r > border or g > border or b > border:
            r = 255
            g = 255
            b = 255
        img2.putpixel((x,y),(r,g,b))
# 最適なレイアウトの検証
y = 11
goodlayout = 11
cntlen = 0
while (y < 13):
    # 画像から文字を読み込む DigitBuilder
    builder = pyocr.builders.LineBoxBuilder(tesseract_layout=y)
    text = tool.image_to_string(img2, lang="eng", builder=builder)
    print("layout:" + str(y))
    if len(text) > 1:
        out = cv2.imread(path)
        pathout = "./result/out_"+str(y)+".jpg"
        for line_box in text:
            for word_box in line_box.word_boxes:
                print(word_box.content)
                cv2.rectangle(out, word_box.position[0], word_box.position[1], (0, 0, 255), 2)
                cv2.imwrite(pathout, out)
    y = y + 1


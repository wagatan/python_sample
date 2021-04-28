# camera.py
# FPVデータ
# 認識エリアの表示
# 抽出文字の正規チェック追加
import cv2
import os
from PIL import Image, ImageOps
import pyocr
import pyocr.builders
import time
from datetime import datetime
# 正規表現
import re

# 文字認識レイアウト
# 0 Orientation and script detection (OSD) only.
# 1 Automatic page segmentation with OSD.
# 2 Automatic page segmentation, but no OSD, or OCR.
# 3 Fully automatic page segmentation, but no OSD. (Default)
# 4 Assume a single column of text of variable sizes.
# 5 Assume a single uniform block of vertically aligned text.
# 6 Assume a single uniform block of text.
# 7 Treat the image as a single text line.
# 8 Treat the image as a single word.
# 9 Treat the image as a single word in a circle.
# 10 Treat the image as a single character.
# 11 Sparse text. Find as much text as possible in no particular order.
# 12 Sparse text with OSD.
# 13 Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.

# インストール済みのTesseractのパスを通す
path_tesseract = "C:\\Program Files\\Tesseract-OCR"
if path_tesseract not in os.environ["PATH"].split(os.pathsep):
    os.environ["PATH"] += os.pathsep + path_tesseract

# OCRエンジンの取得
tools = pyocr.get_available_tools()
tool = tools[0]

# 動画を読込み
# カメラ等でストリーム再生の場合は引数に0等のデバイスIDを記述する
# video = cv2.VideoCapture(1)
video = cv2.VideoCapture("./data/FPV_SRT.mp4")
print(video.get(cv2.CAP_PROP_FPS))

# 文字認識の終了判定用フラグ
cnt = 1

# 認識結果ファイル出力
# 時刻を取得
date = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = "./result/log" + date + ".txt"
f = open(log_file, 'w',newline='\n',encoding='UTF-8')
log_buffer = ""

while video.isOpened():
    # フレームを読込み
    ret, frame = video.read()
    # フレームが読み込めなかった場合は終了（動画が終わると読み込めなくなる）
    if not ret: break
    frame = cv2.resize(frame, dsize=(800, 450)) 

    # フレームの描画
    cv2.imshow('frame', frame)

    # 時刻を取得
    date = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    path = "./result/WORK" + date + ".jpg"
    cv2.imwrite(path, frame) # 文字位置認識用のファイル保存

    # OCR対象の画像ファイルを読み込む
    img = Image.open(path)

    # 画像を読みやすいように加工。
    img = img.convert('RGB')
    size = img.size
    img2 = Image.new('RGB',size)
    # RGBが全て0の場合は黒、全て255(MAX)の場合は白
    border = 105
    for x in range(size[0]):
        for y in range(size[1]):
            r,g,b=img.getpixel((x,y))
            if r > border or g > border or b > border:
                r = 255
                g = 255
                b = 255
            if r < border or g < border or b < border:
                r = 0
                g = 0
                b = 0
            img2.putpixel((x,y),(r,g,b))

    # 画像から文字を読み込む レイアウト
    text = tool.image_to_string(img,lang="eng",builder=pyocr.builders.WordBoxBuilder(tesseract_layout=6))
    # 文字認識の判断で文字列の長さを確認
    out_flg = "no"
    pic_word = ""
    out_path = "./result/" + str(cnt) + "_" + date + ".jpg"
    out = cv2.imread(path)
    for d in text:
        # 英数字から始まり、２文字以上の認識を採用　記号と１文字の認識は除外
        if (len(d.content) > 1) and re.match(r'[a-z,0-9]+', d.content):
            pic_word = pic_word + str(d.content) +","
            # 認識した文字の位置を抽出
            cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2)
            print(d.content)
            out_flg = "yes"
    if(out_flg == "yes"):
        log_buffer = log_buffer + 'Count = ' + str(cnt) + ','
        log_buffer = log_buffer + 'File Name = ' + str(out_path) + ','
        log_buffer = log_buffer + 'WORD:' + pic_word + '\n'
        cv2.imwrite(out_path, out)
        img2.save("./result/" + str(cnt) + "_temp.jpg")
        cnt = cnt + 1
    if cnt > 500: break
    
    os.remove(path)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break

#メモリの解放
video.release()
cv2.destroyAllWindows()

# ログファイルの出力
f.writelines(str(log_buffer))
f.close()

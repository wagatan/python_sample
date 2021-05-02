# 必要なライブラリをインポート
import cv2
import os
import re
from dronekit import connect, VehicleMode, LocationGlobalRelative    # フライトコントローラやシミュレータへ接続するのがdronekit内にあるconnect
import datetime

#OpenCV 顔認識用
#分析ファイル
cascade_path = "C:/python/opencv/haarcascade_frontalface_alt.xml"
work_path = "C:/python/opencv/"
photo_count = 0
max_photo_count = 100
x_pos = 30
y_pos = 30

# ドローンに接続
connection_string = "udp:0.0.0.0:14541"
print( u"FCへ接続: %s" % (connection_string) )    # 接続設定文字列を表示
vehicle = connect(connection_string, wait_ready=False)    # 接続
print(vehicle.mode)
print(vehicle.battery)
print(vehicle.location.global_relative_frame.alt)
print(vehicle.armed)
now = datetime.datetime.now()
now.strftime("%Y/%m/%d %H:%M:%S")
print(now)

# rtspのURL指定でキャプチャするだけ
capture = cv2.VideoCapture('rtsp://10.0.2.100:8554/video')
while(True):
    ret, frame = capture.read()
    bat=re.split('[:=,]', str(vehicle.battery))
    cv2.putText(frame, str(now), (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), thickness=2)
    cv2.putText(frame, str(now), (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), thickness=1)
    cv2.putText(frame, "Voltage:" + bat[2], (x_pos, y_pos + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), thickness=2)
    cv2.putText(frame, "Voltage:" + bat[2], (x_pos, y_pos + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), thickness=1)
    cv2.putText(frame, "Height:" + str(vehicle.location.global_relative_frame.alt), (x_pos, y_pos + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), thickness=2)
    cv2.putText(frame, "Height:" + str(vehicle.location.global_relative_frame.alt), (x_pos, y_pos + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), thickness=1)
    cv2.putText(frame, str(vehicle.mode), (x_pos, y_pos + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), thickness=2)
    cv2.putText(frame, str(vehicle.mode), (x_pos, y_pos + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), thickness=1)
    now = datetime.datetime.now()
    now.strftime("%Y/%m/%d %H:%M:%S")
    # 顔検出
    cascade = cv2.CascadeClassifier(cascade_path)
    facerect = cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
    # 矩形線の色
    rectangle_color = (0, 255, 0) #緑色
    # 顔を検出した場合
    if len(facerect) > 0:
        for rect in facerect:
            cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), rectangle_color, thickness=2)
            date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")
            file_path = work_path + "result/"+ date + ".jpg"
            cv2.imwrite(file_path, frame) 
            photo_count = photo_count + 1 

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if photo_count > max_photo_count:
        break
capture.release()
cv2.destroyAllWindows()

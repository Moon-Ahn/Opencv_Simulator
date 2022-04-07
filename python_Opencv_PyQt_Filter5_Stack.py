#python Version '3.7.6' , opencv Version '4.2.0'

import cv2
import glob
import os.path
import numpy as np
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextBrowser
import itertools

global k
k = 2

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('동영상 재생', self)
        btn2 = QPushButton('Normal && Reset', self)
        btn3 = QPushButton('Median Filter', self)
        btn4 = QPushButton('Gray Filter', self)
        btn5 = QPushButton('Red Filter', self)
        btn6 = QPushButton('Pixel Crol', self)
        btn7 = QPushButton('파일 리스트', self)
        #btn8 = QPushButton('ADD',self)

        btn1.move(600, 20)
        btn1.resize(150, 50)
        btn2.move(600, 100)
        btn2.resize(150, 50)
        btn3.move(600, 180)
        btn3.resize(150, 50)
        btn4.move(600, 260)
        btn4.resize(150, 50)
        btn5.move(600, 340)
        btn5.resize(150, 50)
        btn6.move(600, 420)
        btn6.resize(150, 50)
        btn7.move(600, 500)
        btn7.resize(150, 50)
        #btn8.move(770, 210)
        #btn8.resize(100, 100)

        self.text = QTextBrowser(self)
        self.text.resize(500, 500)
        self.text.move(30,30)

        self.setWindowTitle('Window')
        self.setGeometry(300, 300, 900, 600)
        self.show()

        btn1.clicked.connect(self.Video_Open)
        btn2.clicked.connect(self.Video_Normal)
        btn3.clicked.connect(self.Video_Median)
        btn4.clicked.connect(self.Video_Gray)
        btn5.clicked.connect(self.Video_Red)
        btn6.clicked.connect(self.Video_Pixel)
        btn7.clicked.connect(self.Read_error)

    def Video_Open(self):
        videoFile='C:/Users/ahw/Desktop/sim1/1.mp4'
        cap = cv2.VideoCapture(videoFile)
        #double fps = cap.get(CAP_PROP_FPS)# 동영상 프레임 확인 https://thebook.io/006939/ch04/01/03-01/
        # cap = cv2.VideoCapture(0) #캠화면
        #ret = cap.set(3, 480)  # 캠가로크기 조절
        #ret = cap.set(4, 272)  # 캠세로크기 조절
        winname = "Normal"
        while (cap.isOpened()):
            ret, frame = cap.read()

            if ret:

                ## button filter






                ## 지속되지 않는 영상값을 하고싶다면 filtered를 frame으로 교체하면 됨//






                #cv2.moveWindow(winname, 40, 30)  # 동영상윈도우 위치조정
                #cv2.resizeWindow(winname, 800, 600)
                #print(k)

                if (k == 2) :
                    filtered = frame
                elif (k == 3) :
                    median = cv2.medianBlur(filtered, 5)  # 5x5 median filter
                    filtered = median
                elif (k == 4) :
                    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)  # gray scale
                    filtered = gray
                elif (k == 5) :
                    hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
                    lower_red = cv2.inRange(hsv, (0, 70, 50), (10, 255, 255))
                    upper_red = cv2.inRange(hsv, (170, 70, 50), (180, 255, 255))
                    added_red = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0)
                    red = cv2.bitwise_and(filtered, filtered, mask=added_red)
                    filtered = red
                elif (k == 6) :
                    ######################################bounding box############################################

                    try :
                        hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
                        lower_red = cv2.inRange(hsv, (0, 70, 50), (10, 255, 255))
                        upper_red = cv2.inRange(hsv, (170, 70, 50), (180, 255, 255))
                        added_red = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0)
                        red = cv2.bitwise_and(filtered, filtered, mask=added_red)
                        red_gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)  # gray scale
                        ret, thresh = cv2.threshold(red_gray, 0, 255, cv2.THRESH_BINARY)
                        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        #cnt = contours[1]
                        c = max(contours, key=cv2.contourArea)  # 추가
                        x, y, w, h = cv2.boundingRect(c)  # 추가
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    except ValueError:
                        pass
                    filtered = frame

                cv2.imshow("Camera",filtered)
                #cv2.imshow(winname, frame)
                if cv2.waitKey(20) & 0xFF == ord('q'):  # q누르면 정지
                    break
                # 문제 발견 코드 실행
                if cv2.waitKey(20) & 0xFF == ord('c'):  # 문제가 생겼을 시 (ex 화재)
                    #print('a')
                    now = time.localtime()
                    cv2.imwrite("C:/Users/ahw/Desktop/sim1/%02d_%02d_%02d.jpg" % (now.tm_hour, now.tm_min, now.tm_sec), frame)

            else:
                break

        cap.release()
        cv2.destroyAllWindows()

        f = open("C:/Users/ahw/Desktop/sim1/Error_List.txt", 'w') # jpg파일 읽어서 텍스트에 write
        for a in glob.glob(os.path.join("C:/Users/ahw/Desktop/sim1", "*.jpg")):
            f.write(a)
            f.write("\n")
        f.close()

    # 버튼 함수
    def Video_Normal(self):
        global k
        k = 2
    def Video_Median(self):
        global k
        k = 3
    def Video_Gray(self):
        global k
        k = 4
    def Video_Red(self):
        global k
        k = 5
    def Video_Pixel(self):
        global k
        k = 6
    def Read_error(self): #오류jpg 리스트들을 나태내줌
        myPath = 'C:/Users/ahw/Desktop/sim1'

        myExt = '*.jpg' # 찾고 싶은 확장자
        f = open("Error_List.txt", 'w')
        for a in glob.glob(os.path.join(myPath, myExt)):
            f.write(a)
        f.close()
        #print('a')
        with open('C:/Users/ahw/Desktop/sim1/Error_List.txt', mode="r") as file:
            content = list()

            while True:
                sentence = file.readline()

                if sentence:
                    content.append(sentence)
                else:
                    break
            #print(content)
            t=0
            #print(len(content))4

            for a in content:
                self.text.append(content[int(t)])
                t=t+1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())


# save jpg list file
# def File_Create(myPath, myExt):
#     myPath = '/내가/원하는/디렉토리/경로'
#
#     myExt = '*.jpg' # 찾고 싶은 확장자
#     f = open("Error_List.txt", 'w')
#     for a in glob.glob(os.path.join(myPath, myExt)):
#         f.write(a)
#     f.close()
#     #print('a')
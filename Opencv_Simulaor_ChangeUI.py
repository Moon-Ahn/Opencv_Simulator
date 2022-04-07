#python Version '3.7.6' , opencv Version '4.2.0'

import cv2
import glob
import os.path
import numpy as np
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextBrowser, QComboBox
import itertools

global k
k = 2

def Filters(filter,frame) :

    if (filter == 0) :
        frame = frame
    elif (filter == 1) :
        frame = cv2.medianBlur(frame, 5)
    elif (filter == 2):
        try :
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # gray scale
        except :
            pass
    elif (filter == 3) :

        try :
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_red = cv2.inRange(hsv, (0, 70, 50), (10, 255, 255))
            upper_red = cv2.inRange(hsv, (170, 70, 50), (180, 255, 255))
            added_red = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0)
            frame = cv2.bitwise_and(frame, frame, mask=added_red)

        except :
            pass

    return frame

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('동영상 재생 / 초기화', self)
        self.btn2 = QPushButton('Red Detection', self)
        btn3 = QPushButton('파일 리스트', self)

        self.cb1 = QComboBox(self)
        self.cb1.addItems(['Filter', 'Median', 'Gray', 'Red'])
        self.cb2 = QComboBox(self)
        self.cb2.addItems(['Filter', 'Median', 'Gray', 'Red'])
        self.cb3 = QComboBox(self)
        self.cb3.addItems(['Filter', 'Median', 'Gray', 'Red'])
        self.cb4 = QComboBox(self)
        self.cb4.addItems(['Filter', 'Median', 'Gray', 'Red'])



        btn1.move(700, 70)
        btn1.resize(150, 50)
        self.btn2.move(700, 150)
        self.btn2.resize(150, 50)
        btn3.move(700, 230)
        btn3.resize(150, 50)

        self.cb1.move(50,80)
        self.cb1.resize(100,30)
        self.cb2.move(200, 80)
        self.cb2.resize(100, 30)
        self.cb3.move(350, 80)
        self.cb3.resize(100, 30)
        self.cb4.move(500, 80)
        self.cb4.resize(100, 30)

        self.text = QTextBrowser(self)
        self.text.resize(800, 200)
        self.text.move(50,300)

        self.setWindowTitle('Window')
        self.setGeometry(300, 300, 900, 600)
        self.show()

        btn1.clicked.connect(self.Video_Open)
        self.btn2.setCheckable(True)
        self.btn2.clicked.connect(self.Video_Pixel)
        btn3.clicked.connect(self.Read_error)

    def Video_Open(self):
        videoFile='C:/Users/ahw/Desktop/sim1/1.mp4'


        #print(self.cb1.currentText())
        cap = cv2.VideoCapture(videoFile)
        #double fps = cap.get(CAP_PROP_FPS)# 동영상 프레임 확인 https://thebook.io/006939/ch04/01/03-01/
        # cap = cv2.VideoCapture(0) #캠화면
        #ret = cap.set(3, 480)  # 캠가로크기 조절
        #ret = cap.set(4, 272)  # 캠세로크기 조절
        winname = "Normal"
        while (cap.isOpened()):
            ret, frame = cap.read()

            if ret:



                #cv2.moveWindow(winname, 40, 30)  # 동영상윈도우 위치조정
                #cv2.resizeWindow(winname, 800, 600)
                #print(k)

                #list = [gray,median,red]

                frame = Filters(filter=self.cb1.currentIndex(),frame=frame)
                frame = Filters(filter=self.cb2.currentIndex(), frame=frame)
                frame = Filters(filter=self.cb3.currentIndex(), frame=frame)
                frame = Filters(filter=self.cb4.currentIndex(), frame=frame)

                    ######################################bounding box############################################
                if k == 6 :
                    try:
                        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                        lower_red = cv2.inRange(hsv, (0, 70, 50), (10, 255, 255))
                        upper_red = cv2.inRange(hsv, (170, 70, 50), (180, 255, 255))
                        added_red = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0)
                        red = cv2.bitwise_and(frame, frame, mask=added_red)
                        red_gray = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)  # gray scale
                        ret, thresh = cv2.threshold(red_gray, 0, 255, cv2.THRESH_BINARY)
                        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        # cnt = contours[1]
                        c = max(contours, key=cv2.contourArea)  # 추가
                        x, y, w, h = cv2.boundingRect(c)  # 추가
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    except :
                        pass

                cv2.imshow("Camera",frame)
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
    def Video_Pixel(self,state):
        global k
        if self.btn2.isChecked():
            k = 6
        else:
            k = 2
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
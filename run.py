# 패키지 설치
import cv2
import PIL.Image

from picamera import Color
from picamera import PiCamera
from tkinter import *
import tkinter.font
from os import listdir

import socket
import sys
import os
from time import sleep

global camera
camera = PiCamera()

def delete():
    if os.path.isfile('./picture/0.jpg'):
        os.remove('./picture/0.jpg')
        print('삭제 완료')
    if os.path.isfile('./output.mp4'):
        os.remove('./output.mp4')
        print('mp4 삭제')
    if os.path.isfile('./video.h264'):
        os.remove('./video.h264')
        print('h264 삭제')
    return

def tkinter_close():
    root.destroy()
    
def result(msg):
    
    global root
    root = Toplevel()
    root.overrideredirect(True)
    root.overrideredirect(False)
    root.attributes('-fullscreen', True)
    
    font = tkinter.font.Font(family='맑은 고딕', size=25, weight='bold')
    font1 = tkinter.font.Font(family='맑은 고딕', size=25, weight='bold')
    
    image = tkinter.PhotoImage(file='./images/result.png')
    imgmain = tkinter.PhotoImage(file='./images/main.png')
    
    label = tkinter.Label(root, image=image)
    label.pack()

    label2 = tkinter.Label(root, text=msg,
                           font=font1, fg='white', bg='#3B3838')
    label2.place(x=125, y=100)

    btFi = Button(root, bg='#D9D9D9', image=imgmain, bd=0,command=tkinter_close,
                  activebackground='#D9D9D9')
    btFi.place(x=250, y=325)

    root.after(10000, lambda: root.destroy())
    root.mainloop()
    
def transfer(check):
    try:
        # 전송시킬 이미지 경로 설정
        capture_file_name = os.getcwd() + '/picture/0.jpg'
        
        # 서버 연결
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect(('220.69.241.86', 11000))
        
        # img 가져오기 보낼 (파일경로/이름)
        file = open(capture_file_name, 'rb')
        img_size = os.path.getsize(capture_file_name)
        img = file.read(1024) # 저장된 이미지를 읽는다.

        # 장소 설정 및 입/퇴실 여부 서버 전송
        if check == 0:
            place = '0|000000003e8ac9f3'
        else:
            place = '1|000000003e8ac9f3'
        place = place.encode('utf-8')
        c.send(place)
        print('장소를 전송')
        c.recv(1024)
        print('장소 확인 완료')
        
        # 데이터 전송
        while (img):
            print('전송중...')
            c.send(img)
            img = file.read(1024)
        file.close()
        print('이미지 전송 완료.')
        c.shutdown(socket.SHUT_WR)
        
        # 데이터 수신
        data = c.recv(1024).decode('utf-8')
        spl = data.split('|')
        print(spl[0])
        
        # 각 입실, 퇴실에 대한 msg 전송
        if spl[0] == '0':
            spl[0] = '퇴실'
            msg = '{} {} {}님이\n {}에 {}에 {}하셨습니다.'.format(spl[1],spl[2],spl[3],
                                                         spl[4],spl[5],spl[0])
        elif spl[0] == '1':
            spl[0] = '입실'
            msg = '{} {} {}님이\n {}에 {}에 {}하셨습니다.'.format(spl[1],spl[2],spl[3],
                                                         spl[4],spl[5],spl[0])
        elif spl[0] == '2':
            msg = '         얼굴을 인식하지 못하였습니다.\n         다시 시도해주세요.'
        elif spl[0] == '3':
            msg = '         등록되지 않은 얼굴입니다.\n          등록후 사용해주세요.'
        elif spl[0] == '4':
            msg = '         이미 입실이 되어 있습니다.'
        elif spl[0] == '5':
            msg = '         입실이 되어있지 않습니다.\n          입실 후 사용해주세요.'
        elif spl[0] == '6':
            msg = '         이미 퇴실이 되어 있습니다.'
            
        # print(data[2:])
        print(msg)

        # 서버와 연결 종료
        c.close()
    #    print('전송 완료')
    except ConnectionRefusedError:
        print('서버와 연결이 되지 않았습니다..')
        msg = '         서버와 연결되지 않았습니다.'
        delete()
        return msg
    # 폴더에 사진을 다시 찍어주기 위해 삭제 해준다.
#    if os.path.isfile(capture_file_name):
#        os.remove(capture_file_name)
#        print('삭제 완료')
    delete()
    
    
    return msg

# 얼굴을 인식할시 인식할 얼굴을 이미지에 저장
def address(check):
    cascade = cv2.CascadeClassifier('./xml/haarcascade_frontalface_default.xml')
    pat = '/home/pi/Final_Project/picture'
    file_list = []
    
# 파이 카메라 설정    
    camera.brightness = 60
    camera.resolution = (800, 480)
    camera.framerate = 15
    camera.hflip = True
    camera.start_preview()

# picture 폴더에 파일이 하나있을 때까지 실행된다.
    while len(file_list)<1:
        a = 1
        file_list = os.listdir(pat)
        camera.start_recording('video.h264')
        sleep(1)
        camera.stop_recording()
        os.system('MP4Box -add video.h264 output.mp4')
        
        cap = cv2.VideoCapture('output.mp4')
        
        while True:
            # 영상을 읽기 위한 frame 생성
            ret, frame = cap.read()
            
            try:                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = cascade.detectMultiScale(gray, 1.3, 5)
            except cv2.error:
                print('frame error 발생')
                delete()
                break
            
            if not frame is None:
                if len(faces)>0:
                    for face in faces:
                        x,y,w,h = face
# [y-10:y+h+10, x-10:x+w+10]
                    cv2.imwrite(pat+'/'+'0.jpg', frame)
#                    image = PIL.Image.open(pat+'/'+'0.jpg')
#                    resize_image = image.resize((128, 128))
#                    resize_image.save(pat+'/'+'0.jpg')
                    global msg
                    msg = transfer(check)
                    camera.stop_preview()
                    return
            else:
                delete()
                print('frame 오링낫다구')
                break
                
            
# 함쑤 시작드
def start(check):
    delete()
    address(check)
    result(msg)

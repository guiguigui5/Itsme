from tkinter import *
import tkinter.font
from run import *

import PIL.Image

# 메인 인터페이스 생성
root = Tk()

# tk 전체화면으로 띄우기
root.overrideredirect(True)
root.overrideredirect(False)
root.attributes('-fullscreen', True)

# font 부분
font=tkinter.font.Font(family='맑은 고딕', size=25, weight='bold')

# 이미지 뒤의 background 부분
img = tkinter.PhotoImage(file='./images/itsme.png')
imgin = tkinter.PhotoImage(file='./images/in.png')
imgout = tkinter.PhotoImage(file='./images/out.png')

label = tkinter.Label(root, image=img)
label.pack()

# 입실, 퇴실 버튼 부분
bt1 = Button(root, bg='#D9D9D9', bd=0, image=imgin, command=lambda: start(1),
             activebackground= '#D9D9D9')
bt1.place(x=500, y=120)


bt2 = Button(root, bg='#D9D9D9', bd=0, image=imgout, command=lambda: start(0),
             activebackground= '#D9D9D9')
bt2.place(x=500, y=300)

# 윈도우 창이 종료될 때까지 실행
root.mainloop()

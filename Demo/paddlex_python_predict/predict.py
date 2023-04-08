# 脚本运行依赖paddlex
# pip install paddlex
import random
import time
import queue
import threading
import win32api

import win32gui
from win32gui import *  # 操作windows窗口
from PIL import ImageGrab  # 操作图像
import win32con  # 系统操作

import paddlex as pdx
import cv2
import  numpy as np
import pyautogui

print("Loading model...")
model = pdx.load_model('inference_model')
print("Model loaded.")

#im = cv2.imread('test.jpg')
#im = im.astype('float32')

#result = model.predict(im)
class VideoCapture:
    """Customized VideoCapture, always read latest frame"""

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue(maxsize=1)
        self.stop_threads = False  # to gracefully close sub-thread
        th = threading.Thread(target=self._reader)
        th.daemon = True  # 设置工作线程为后台运行
        th.start()

    # 实时读帧，只保存最后一帧
    def _reader(self):
        while not self.stop_threads:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

    def terminate(self):
        self.stop_threads = True
        self.cap.release()

def move(x, y):
  """
  函数功能：移动鼠标到指定位置
  参  数：x:x坐标
       y:y坐标
  """
  win32api.SetCursorPos((x, y))


def get_cur_pos():
  """
  函数功能：获取当前鼠标坐标
  """
  p={"x":0,"y":0}
  pos = win32gui.GetCursorPos()
  p['x']=pos[0]
  p['y']=pos[1]
  return p


def left_click():
  """
  函数功能：鼠标左键点击
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def right_click():
  """
  函数功能：鼠标右键点击
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN | win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


def left_down():
  """
  函数功能：鼠标左键按下
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def left_up():
  """
  函数功能：鼠标左键抬起
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def right_down():
  """
  函数功能：鼠标右键按下
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)


def right_up():
  """
  函数功能：鼠标右键抬起
  """
  win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)




def get_window_pos(name):
    name = name
    handle = win32gui.FindWindow(0, name)
    # 获取窗口句柄
    if handle == 0:
        return None
    else:
    # 返回坐标值和handle
        return win32gui.GetWindowRect(handle), handle
(x1, y1, x2, y2), handle = get_window_pos('Disney Dreamlight Valley')
win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
# 发送还原最小化窗口的信息
win32gui.SetForegroundWindow(handle)
# 设为高亮

from PIL import Image, ImageGrab



'Disney Dreamlight Valley'
# 可视化结果, 对于检测、实例分割务进行可视化
if model.model_type == "detector":

    cap=VideoCapture(0)
    cap.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cap.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
    cap.cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
    nofinsh = 0
    while True:

        mat = cap.read()
        #img_ready = ImageGrab.grab((x1, y1, x2, y2))
        # 截图
        #print(img_ready)

        #mat=cv2.cvtColor(np.asarray(img_ready), cv2.COLOR_RGB2BGR)
        #mat=cv2.copyMakeBorder(mat,0,560,0,0,0)

        #cv2.imwrite('d:\\111.png',mat)
        m1=0
        m2=0
        m3=0
        #print(nofinsh)
        if nofinsh>=200:
            right_down()
            time.sleep(3)
            right_up()
            nofinsh=0
            continue
        fn=random.randint(0,10000)
        res = model.predict(mat)
        for r in res:
            cate=r.get('category_id')
            score=r.get('score')
            if score>0.5:
                #cv2.rectangle(mat,(0,0),(50,50),(255,0,0),1)
                if cate==0:m1=m1+1
                if cate==1:m2=m2+1
                if cate==2:m3=m3+1

        if m1>0 and m3>1:
            print('收杆')

            nofinsh=0
            #time.sleep(0.05)
            left_down()
            left_down()
            #cv2.imwrite('d:\\123'+str(fn)+'.jpg',mat)
            time.sleep(0.01)
            left_up()
            time.sleep(0.5)
        elif m2>5:
            print('钓鱼完成')
            left_down()
            #cv2.imwrite('d:\\1234' + str(fn) + '.jpg',mat)

            for i in range(5):
                time.sleep(0.01)
                left_up()
                left_down()
            time.sleep(1)
            right_down()


            time.sleep(1)
            right_up()
            right_up()
            left_up()
            nofinsh = 0
            nofinsh=0
            mat = cap.read()
            mat = cap.read()
            mat = cap.read()
            mat = cap.read()
        else:
            nofinsh=nofinsh+1
        #time.sleep(0.5)
        #print(end - start, 'ms')
        #print(res)
       # print(111)
    # threshold用于过滤低置信度目标框
    # 可视化结果保存在当前目录
    #pdx.det.visualize(im, result, threshold=0.5, save_dir='./')
    #print(result)



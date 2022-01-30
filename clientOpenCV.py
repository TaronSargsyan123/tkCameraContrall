import time
from threading import *
import PIL
from PIL import Image, ImageTk
import cv2
import numpy
from firmata import *

class OpenCVcamera:
    def __init__(self, camera, videoPanel, x, y):
        self.width = x
        self.heigth = y
        self.videoPanel = videoPanel
        self.cap = cv2.VideoCapture(camera)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, x)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, y)

        self.thread = Thread(target=self.detectFace)
        self.showVideo()

        self.faceStage = False




    def showVideo(self):
        try:
            self.firmata = firmata()
            self.ret, self.frame = self.cap.read()
            self.frame = cv2.flip(self.frame, 1)
            self.cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)


            self.img = PIL.Image.fromarray(self.cv2image)
            self.imgtk = ImageTk.PhotoImage(image=self.img)
            self.videoPanel.imgtk = self.imgtk
            self.videoPanel.configure(image=self.imgtk)
            self.videoPanel.after(10, self.showVideo)
        except:
            self.videoPanel.configure(text="Video capture ERROR")

    def faceDetectOn(self):
        self.thread.start()




    def detectFace(self):


        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


        firstLineX = self.width // 3
        secondLineX = (self.width // 3) * 2

        firstLineY = self.heigth // 3
        secondLineY = (self.heigth // 3) * 2

        while True:

            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)

            for (x, y, w, h) in faces:
               cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

               if x > secondLineX:
                   try:
                        self.firmata.right(1)
                   except:
                        print("right")

               elif x < firstLineX:
                   self.firmata.left(1)
                   print("left")

               elif y < firstLineY:
                   print("up")
                   self.firmata.up(1)

               elif y > secondLineY:
                   print("down")
                   self.firmata.down(1)

               else:
                   stage = "center"
                   print("centre")



    def faceDetectOff(self):
        self.thread.join()





import tkinter as tk
from tkinter import ttk
from clientOpenCV import OpenCVcamera
from firmata import firmata
from threading import *

class mainWindow:
    def __init__(self):
        self.__width = 1130
        self.__height = 540

        self.camera = 1
        self.test = False

        #colors
        self.color1 = "#27292D"
        self.color2 = "#38393D"
        self.colorFont = "#4D7992"

        self.faceStage = 1
        self.colorStage = 1

            

        self.initWindow()
        self.createWidgets()
        self.placeWidgets()
        self.firmata = firmata()


        self.tryFirmata()



        self.window.mainloop()



    def tryFirmata(self):
        try:
            self.firmata.initFirmata()
        except:
            print("COM port not detected")
            self.controlButtonsCanvas.place_forget()
            self.camera = 0

    def getWidth(self):
        return self.__width

    def setWidth(self, value):
        self.__width = value

    def getHeight(self):
        return self.__height

    def setHeight(self, value):
        self.__height = value

    def initWindow(self):
        self.window = tk.Tk()
        self.window.geometry(str(self.getWidth())+"x"+str(self.getHeight()))
        self.window.minsize(str(self.getWidth()), str(self.getHeight()))
        self.window.title("camera control system")
        self.window.wm_iconbitmap("sprites/icon.png")
        self.window.resizable(False, False)
        self.window["bg"] = "#38393D"
        self.window.bind('<Escape>', lambda e: self.window.quit())

    def createWidgets(self):
        #sprites 100x100
        self.btnUpIMG = tk.PhotoImage(file=r"sprites/btnUp.png")
        self.btnDownIMG = tk.PhotoImage(file=r"sprites/btnDown.png")
        self.btnLeftIMG = tk.PhotoImage(file=r"sprites/btnLeft.png")
        self.btnRightIMG = tk.PhotoImage(file=r"sprites/btnRight.png")
        self.centreLabelIMG = tk.PhotoImage(file=r"sprites/labelCenter.png")

        self.colorOnIMG = tk.PhotoImage(file=r"sprites/colorOn.png")
        self.colorOffIMG = tk.PhotoImage(file=r"sprites/colorOff.png")
        self.faceOnIMG = tk.PhotoImage(file=r"sprites/faceOn.png")
        self.faceOffIMG = tk.PhotoImage(file=r"sprites/faceOff.png")

        #canvases
        self.rightCanvas = tk.Canvas(self.window, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        self.controlButtonsCanvas = tk.Canvas(self.rightCanvas, bg=self.color1, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        self.leftCanvas = tk.Canvas(self.window, bg=self.color1, relief=tk.FLAT, borderwidth=0, highlightthickness=0)
        self.faceAndColorDetectionCanvas = tk.Canvas(self.rightCanvas, bg=self.color1, relief=tk.FLAT, borderwidth=0, highlightthickness=0)

        #control buttons

        self.upButton = tk.Button(self.controlButtonsCanvas, relief=tk.FLAT, borderwidth=0, activebackground="#27292D", image=self.btnUpIMG, bg=self.color1, command=self.up)
        self.downButton = tk.Button(self.controlButtonsCanvas, relief=tk.FLAT, borderwidth=0, activebackground="#27292D", image=self.btnDownIMG, bg=self.color1, command=self.down)
        self.leftButton = tk.Button(self.controlButtonsCanvas, relief=tk.FLAT, borderwidth=0, activebackground="#27292D", image=self.btnLeftIMG, bg=self.color1, command=self.left)
        self.rightButton = tk.Button(self.controlButtonsCanvas, relief=tk.FLAT, borderwidth=0, activebackground="#27292D", image=self.btnRightIMG, bg=self.color1, command=self.right)
        self.centralLabel = tk.Label(self.controlButtonsCanvas, relief=tk.FLAT, borderwidth=0, activebackground="#27292D", image=self.centreLabelIMG, bg=self.color1)




        self.faceDetectionButton = tk.Button(self.faceAndColorDetectionCanvas, bg=self.color1, relief=tk.FLAT, borderwidth=0, activebackground="#27292D", fg=self.colorFont, image=self.faceOffIMG, command=self.faceDetection)
        self.colorDetectionButton = tk.Button(self.faceAndColorDetectionCanvas, bg=self.color1, relief=tk.FLAT, borderwidth=0, activebackground="#27292D", fg=self.colorFont, image=self.colorOffIMG, command=self.colorDetection)

        #video lable
        self.videoLable = tk.Label(self.leftCanvas, bg="red")

        #combobox
        self.comboList = ttk.Combobox(self.leftCanvas, style="TCombobox")
        self.comboList['values'] = ["webcam", "com4"]
        self.comboList.current(0)

        self.stageButton = tk.Button(self.leftCanvas, relief=tk.FLAT, borderwidth=0, text="OK", bg=self.color2, command=self.stage, fg=self.colorFont, activebackground=self.color1)





    def placeWidgets(self):
        self.leftCanvas.place(x=10, y=10, width=750, height=520)
        self.videoLable.place(x=0, y=0, width=750, height=520)
        self.rightCanvas.place(x=770, y=10, width=350, height=520)
        self.controlButtonsCanvas.place(x=0, y=0, width=350, height=350)
        self.faceAndColorDetectionCanvas.place(x=0, y=350, width=350, height=170)

        self.upButton.place(x=125, y=12.5, width=100, height=100)
        self.leftButton.place(x=12.5, y=125, width=100, height=100)
        self.rightButton.place(x=237.5, y=125, width=100, height=100)
        self.downButton.place(x=125, y=237.5, width=100, height=100)
        self.centralLabel.place(x=125, y=125, width=100, height=100)


        self.faceDetectionButton.place(x=10, y=10, width=330, height=70)
        self.colorDetectionButton.place(x=10, y=90, width=330, height=70)

        self.comboList.place(x=10, y=10, width=100, height=30)
        self.stageButton.place(x=120, y=10, width=30, height=30)

    def faceDetection(self):
        if self.faceStage == 1:

            self.faceOn()
            self.colorOff()
        elif self.faceStage == 2:
            self.faceOff()

    def colorDetection(self):
        if self.colorStage == 1:
            self.colorOn()
            self.faceOff()
        elif self.colorStage == 2:
            self.colorOff()

    def faceOn(self):

        #ui logic
        self.faceDetectionButton.configure(image=self.faceOnIMG)
        self.faceStage = 2

        #work logic
        self.OpenCVcamera.faceDetectOn()


    def faceOff(self):
        # ui logic
        self.faceDetectionButton.configure(image=self.faceOffIMG)
        self.faceStage = 1


        # work logic
        self.OpenCVcamera.faceDetectOff()

    def colorOn(self):
        # ui logic
        self.colorDetectionButton.configure(image=self.colorOnIMG)
        self.colorStage = 2

        # work logic

    def colorOff(self):
        # ui logic
        self.colorDetectionButton.configure(image=self.colorOffIMG)
        self.colorStage = 1

        # work logic

    def left(self):
        if self.camera == 1:
            self.colorOff()
            self.faceOff()
            self.firmata.left(10)

    def right(self):
        if self.camera == 1:
            self.colorOff()
            self.faceOff()
            self.firmata.right(10)

    def up(self):
        if self.camera == 1:
            self.colorOff()
            self.faceOff()
            self.firmata.up(10)

    def down(self):
        if self.camera == 1:
            self.colorOff()
            self.faceOff()
            self.firmata.down(10)

    def stage(self):
        if self.comboList.get() == "com4":
            self.OpenCVcamera = OpenCVcamera(0, self.videoLable, 426, 240).cap.release()
            self.camera = 1
            self.controlButtonsCanvas.place(x=0, y=0, width=350, height=350)
            self.OpenCVcamera = OpenCVcamera(1, self.videoLable, 426, 240)
            print(self.camera)
        elif self.comboList.get() == "webcam":
            self.OpenCVcamera = OpenCVcamera(1, self.videoLable, 426, 240).cap.release()
            self.camera = 0
            self.controlButtonsCanvas.place_forget()
            self.OpenCVcamera = OpenCVcamera(0, self.videoLable, 426, 240)
            print(self.camera)
        else:
            pass


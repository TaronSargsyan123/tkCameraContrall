import cv2
import os
import pyfirmata
import serial.tools.list_ports as ports

class firmata:
    def __init__(self):
        pass


    def initFirmata(self):
        self.board = pyfirmata.Arduino('COM4')

        self.iter8 = pyfirmata.util.Iterator(self.board)
        self.iter8.start()

        self.pin9 = self.board.get_pin('d:9:s')
        self.pin10 = self.board.get_pin('d:10:s')

        self.xAngle = 90
        self.yAngle = 100


        self.setStartPosition()
        print(self.choseComPort())


    def moveServo(self, angle, pin):
        pin.write(angle)

    def setStartPosition(self):
        self.moveServo(self.xAngle, self.pin9)
        self.moveServo(self.yAngle, self.pin10)


    def right(self, value):
        if self.xAngle < 175-value:
            self.xAngle = self.xAngle + value
            self.moveServo(self.xAngle, self.pin9)
        print("right")

    def left(self, value):
        if self.xAngle > value:
            self.xAngle = self.xAngle - value
            self.moveServo(self.xAngle, self.pin9)
        print("left")

    def up(self, value):
        if self.yAngle > value:
            self.yAngle = self.yAngle - value
            self.moveServo(self.yAngle, self.pin10)
        print("up")

    def down(self, value):
        if self.yAngle < 175 - value:
            self.yAngle = self.yAngle + value
            self.moveServo(self.yAngle, self.pin10)
        print("down")

    def choseComPort(self):
        com_ports = list(ports.comports())
        self.list = []
        for i in com_ports:
            self.list.append(i.device)

        print(self.list)

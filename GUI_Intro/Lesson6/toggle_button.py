#!/usr/bin/python3

#Push button that is either on or off, mostly comsetic differences from check box


import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QApplication
from PyQt5.QtGui import QColor

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #set initial color to black
        self.col = QColor(0, 0, 0)

        #create push button object
        redb = QPushButton('Red', self)
        #make button like a check box, either true or false
        redb.setCheckable(True)
        redb.move(10, 10)

        #connect our function to set color to signal from the button using the boolean version of the signal
        redb.clicked[bool].connect(self.setColor)

        greenb = QPushButton('Green', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)

        greenb.clicked[bool].connect(self.setColor)

        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)

        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Toggle button')
        

    def setColor(self, pressed):

        #get the value of the sender of the signal
        source = self.sender()

        #turn color on or off
        if pressed:
            val = 255
        else:
            val = 0

        #get value of the button that was pressed
        if source.text() == "Red":
            self.col.setRed(val)
        elif source.text() == "Green":
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)

        #tag inside background-color must match exactly!! no changes to spacing or syntax!
        self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

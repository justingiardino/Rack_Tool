#!/usr/bin/python3

#Show a slider widget


import sys
from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #create horizontal slider
        sld = QSlider(Qt.Horizontal, self)
        sld. setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        #connect integer version of valueChanged signal to our defined function changeValue
        sld.valueChanged[int].connect(self.changeValue)

        #create label and add an image to it
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('mute.png'))
        self.label.setGeometry(160, 40, 80, 30)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Slider')
        
    #based on the value of the slider we set a different image in the label
    def changeValue(self, value):
        
        if value == 0:
            self.label.setPixmap(QPixmap('mute.png'))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap('min.png'))
        elif value > 30 and value <= 80:
            self.label.setPixmap(QPixmap('med.png'))
        else:
            self.label.setPixmap(QPixmap('max.png'))
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

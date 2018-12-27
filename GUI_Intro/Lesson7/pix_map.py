#!/usr/bin/python3

#Display photo using pixmap widget


import sys
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication
from PyQt5.QtGui import QPixmap

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        hbox = QHBoxLayout(self)
        #create pixmap object using file name of picture
        pixmap = QPixmap('logo.png')

        #place the pixmap in the label box for display
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        #add the image to the hbox object
        hbox.addWidget(lbl)
        #set size of window equal to the size of the hbox
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Logo')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

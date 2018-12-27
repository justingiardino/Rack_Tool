#!/usr/bin/python3

#Change user input box to color


import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QColorDialog, QFrame
from PyQt5.QtGui import QColor

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        col = QColor(0,0,0)

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20,20)
        #connect btn push signal to showDialog function
        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())
        self.frm.setGeometry(130,22,100,100)

        self.setGeometry(300,300, 250, 180)
        self.setWindowTitle('Color Dialog')

    def showDialog(self):

        col = QColorDialog.getColor()

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }" % col.name())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

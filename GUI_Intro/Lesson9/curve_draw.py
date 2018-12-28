#!/usr/bin/python3

#show curve drawing

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        self.setGeometry(300, 300, 355, 280)
        self.setWindowTitle('Pen Styles')
        self.show()

    #reimplement function
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.drawBezierCurve(qp)
        qp.end()

    def drawBezierCurve(self, qp):

        #create curve with painter path
        path = QPainterPath()
        path.moveTo(30,30)
        #start point, control point, end point
        path.cubicTo(30, 30, 200, 350, 350, 30)
        qp.drawPath(path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exec_()

#!/usr/bin/python3

#show different pen styles

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):


        self.setGeometry(300, 300, 280, 270)
        self.setWindowTitle('Pen Styles')

    #reimplement function
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    #uses predefined pen styels and then creates a custom pen at the end
    def drawLines(self, qp):

        #create a pen object with color black, pixel width of two and uses predefined solidline pen style
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        qp.setPen(pen)
        qp.drawLine(20, 40, 250, 40)

        pen.setStyle(Qt.DashLine)
        qp.setPen(pen)
        #draw line is start_x, start_y, end_x, end_y
        qp.drawLine(20, 100, 250, 60)

        pen.setStyle(Qt.DashDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 120, 250, 120)

        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        qp.drawLine(20, 160, 250, 160)

        pen.setStyle(Qt.DashDotDotLine)
        qp.setPen(pen)
        qp.drawLine(20, 200, 250, 200)

        pen.setStyle(Qt.CustomDashLine)
        pen.setDashPattern([1, 4, 5, 4])
        qp.setPen(pen)
        qp.drawLine(20, 240, 250, 240)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()

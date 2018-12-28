#!/usr/bin/python3

#create a custom widget and signal

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QSlider, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPainter, QFont, QColor, QPen
from PyQt5.QtCore import Qt, QObject, pyqtSignal


class Communicate(QObject):
    updateBW = pyqtSignal(int)

#This is the custom QWidget class we are creating
#widget will graphically showing the capacity
#draw color based on where slider is at
#base this widget on QWidget
class BurningWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #set minimum size to be a bit bigger
        self.setMinimumSize(1,30)
        self.value = 75
        self.num = [75, 150, 225, 300, 375, 450, 525, 600, 675]

    def setValue(self, value):
        self.value = value

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawWdiget(qp)
        qp.end()

    def drawWdiget(self, qp):

        MAX_CAPACITY = 700
        OVER_CAPACITY = 750

        #set size of font
        font = QFont('Serif', 7, QFont.Light)
        qp.setFont(font)

        #dynamically draw widget
        #drawing consists of three steps: draw red and yellow rectangle, draw vertical lines in widget to divide it, and draw the numbers on for capacity
        #if you resize the window, this will resize the status bar
        size = self.size()
        w = size.width()
        h = size.height()

        #create step variable by splitting the width into 10
        step = int(round(w / 10))

        #till is the total size that needs to be drawn
        till = int(((w / OVER_CAPACITY) * self.value))
        #full is where we draw the red color
        full = int(((w / OVER_CAPACITY) * MAX_CAPACITY))

        #when the value is over capacity we need to draw red and yellow
        if self.value >= MAX_CAPACITY:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(0, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full, 0, till-full, h)

        #else only draw yellow
        else:
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 185))
            qp.drawRect(0, 0, till, h)

        pen = QPen(QColor(20, 20, 20), 1, Qt.SolidLine)

        #create invisible rectangle
        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)

        j = 0

        #use fontMetrics to draw on the numbers
        for i in range(step, 10 * step, step):
            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            #add number label at center of vertical line
            qp.drawText(i - fw / 2, h / 2, str(self.num[j]))
            j += 1

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        OVER_CAPACITY = 750

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(1, OVER_CAPACITY)
        sld.setValue(75)
        sld.setGeometry(30, 40, 150, 30)

        self.c = Communicate()
        self.wid = BurningWidget()
        self.c.updateBW[int].connect(self.wid.setValue)

        sld.valueChanged[int].connect(self.changeValue)
        hbox = QHBoxLayout()
        #add widget!
        hbox.addWidget(self.wid)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 390, 210)
        self.setWindowTitle('Burning Widget')
        self.show()

    #when slider is moved, changeValue is called
    def changeValue(self, value):

        #emit our own custom signal
        self.c.updateBW.emit(value)
        self.wid.repaint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

#!/usr/bin/python3

#Drag and drop a button
#click button with left, drag with right

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class Button(QPushButton):
    def __init__(self, title, parent):
        super().__init__(title, parent)

    #reimplementing mouseMoveEvent
    def mouseMoveEvent(self, e):

        #only finish this function if the button pressed on the mouse is the right click
        if e.buttons() != Qt.RightButton:
            return

        mimeData = QMimeData()
        #create QDrag object to be support MIME based drag and drop
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        #when the exec_ method of the drag object starts that begins the drag and drop operation
        dropAction = drag.exec_(Qt.MoveAction)

    #if there is a left click print a console message
    def mousePressEvent(self, e):
        #calle mousePressEvent on parent as well, otherwise we would see the button press
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            print('press')


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setAcceptDrops(True)

        self.button = Button('Button', self)
        self.button.move(100, 65)

        self.setGeometry(300, 300, 280, 150)
        self.setWindowTitle('Click or Move')

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.button.move(position)

        e.setDropAction(Qt.MoveAction)
        e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()

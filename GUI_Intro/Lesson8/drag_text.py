#!/usr/bin/python3

#Drag and drop text
#beginning of multiple classes in a file

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLineEdit

#extra class!
#need to do this sinve we are reimplementing some methods
class Button(QPushButton):
    def __init__(self, title, parent):
        #input parameters that are passed when creating an object of this class
        super().__init__(title, parent)
        #enable drop events for the widget
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        #reimplementing dragEnterEvent, only allowing a certain type of data to be entered
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    #reimplementing what happense when dropEvent is triggered
    def dropEvent(self, e):
        #set text of button widget
        self.setText(e.mimeData().text())


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #QLineEdit has a built in support for drag and drop
        edit = QLineEdit('', self)
        #just have to enable with this function
        edit.setDragEnabled(True)
        edit.move(30, 65)

        #create object of Button class
        button = Button('Button', self)
        button.move(190, 65)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Drag and Drop window')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

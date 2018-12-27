#!/usr/bin/python3

#Check box to display title


import sys
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtCore import Qt

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #construct QCheckBox object
        cb = QCheckBox('Show Title', self)
        cb.move(20,20)
        #toggle will invert current state, since this object is false by default, this will toggle to true
        cb.toggle()
        #connect signal to function changeTitle function
        cb.stateChanged.connect(self.changeTitle)

        self.setGeometry(300,300, 250, 180)
        self.setWindowTitle('Check Box')


    def changeTitle(self, state):

        #state of the widget is stored in the state variable
        #will need to know signal variables like state for widgets like this
        if state == Qt.Checked:
            self.setWindowTitle('Check Box Title!')
        else:
            self.setWindowTitle('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

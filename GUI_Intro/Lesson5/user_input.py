#!/usr/bin/python3

#ask for user input


import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QInputDialog

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20,20)
        #connect btn push signal to showDialog function
        self.btn.clicked.connect(self.showDialog)

        #value entered by user will be displayed in this widget
        self.le = QLineEdit(self)
        self.le.move(130,22)

        self.setGeometry(300,300, 290, 150)
        self.setWindowTitle('Input Dialog')

    def showDialog(self):

        #this will display the input prompt. First string is the title of the box, the second string is the message within the dialog
        #return values are the string of the response and a boolean variable that is true when the user clicks on Ok
        text, ok = QInputDialog.getText(self, 'Input Dialog Box', 'Enter your name: ')

        #if user clicks Ok, update widget display
        if ok:
            #set text for line edit widget
            self.le.setText(str(text))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

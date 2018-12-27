#!/usr/bin/python3

#Display monthly calendar widget and allow user to pick a date


import sys
from PyQt5.QtWidgets import QWidget, QCalendarWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import QDate

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout(self)

        #create QCalendarWidget object
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        #connect QDate version of calendar clicked signal to our showDate function
        #this signal occurs when we select a date from the widget
        cal.clicked[QDate].connect(self.showDate)

        vbox.addWidget(cal)

        self.lbl = QLabel(self)
        #use selectedDate method to retreive the date value, store in local variable date
        date = cal.selectedDate()
        #force date to be a string for printing
        self.lbl.setText(date.toString())

        vbox.addWidget(self.lbl)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Calendar')

    def showDate(self, date):

        self.lbl.setText(date.toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

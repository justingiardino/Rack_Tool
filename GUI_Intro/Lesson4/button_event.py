#!/usr/bin/python3

#display message based on which button was pressed

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton

class Example(QMainWindow):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		btn1 = QPushButton('Button1', self)
		btn1.move(30,50)
		btn2 = QPushButton('Button2', self)
		btn2.move(150,50)

		#when one of the buttons is clicked (the signal) connect to buttonClicked function
		btn1.clicked.connect(self.buttonClicked)
		btn2.clicked.connect(self.buttonClicked)
		#create status bar for later display
		self.statusBar()

		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('Buttons')

	def buttonClicked(self):
		#determine the source of the signal
		sender = self.sender()
		self.statusBar().showMessage(sender.text() + ' was pressed.')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

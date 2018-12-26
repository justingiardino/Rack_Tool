#!/usr/bin/python3

#display x and y coordinates of mouse
#using event objects

import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton

class Communicate(QObject):
	closeApp = pyqtSignal()

class Example(QMainWindow):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		#create custom close app signal
		self.c = Communicate()
		#connect custom event to close
		self.c.closeApp.connect(self.close)


		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('Emit custom signal')

	#when the mouse is clicked emit the close app signal
	def mousePressEvent(self,event):
		self.c.closeApp.emit()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

#!/usr/bin/python3

#Move main application window to center of the screen

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication


class Example(QWidget):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		#set size, not going to use set geometry here since we will be defining the window location separately
		self.resize(250,150)
		
		#call center function we create
		self.center()
		self.setWindowTitle('Center Screen')
	
	#center function finds the center pixel and puts the window there
	def center(self):
		
		#rectangle object the size of the current main window
		qr = self.frameGeometry()
		#Determine the screen resolution of the monitor and grab the center point(cp)
		cp = QDesktopWidget().availableGeometry().center()
		#set the center of the rectangle object to the center point of the screen
		qr.moveCenter(cp)
		#Move the top left point of the main window to the top left of the temporary rectangle object
		#This is because the start point of the window is the top left corner and the rectangle object is the same size as the application window
		self.move(qr.topLeft())
		
	
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

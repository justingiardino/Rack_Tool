#!/usr/bin/python3

#Combine all parts of lesson 1
#Create Window
#Add button
#Tool tip on button
#Quit button 
#Message when closing window 
#Center the window

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMessageBox, QPushButton, QToolTip


class Example(QWidget):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		#set size, not going to use set geometry here since we will be defining the window location separately
		self.resize(300,500)
		
		#call center function we create
		self.center()
		self.setWindowTitle('Lesson 1')
	
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
	
	#closeEvent triggered when QWidget is closed
	def closeEvent(self, event):
	
		reply = QMessageBox.question(self, 'Warning', 'Are you sure to quit?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
		
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()
			
	#Quit does not display a warning
	def addQuitButton(self):
		#create a quit button, still just a pushbutton object
		qbtn = QPushButton('Quit', self)
		#part of event processing system of PyQt5
		qbtn.clicked.connect(QApplication.instance().quit)
        #button size and location
		qbtn.resize(qbtn.sizeHint())
		#move to x location by y location
		#may want to change this to a center function or something instead of statically defining pixel locations
		qbtn.move(125, 450)
		qbtn.setToolTip('This is the Quit button, it will not warn you about saving.')
		
	def addButton(self):
		btn = QPushButton('Add', self)
		btn.resize(btn.sizeHint())
		btn.move(50,100)
		
	def addButtonWithName(self, temp_name):
		btn = QPushButton(temp_name, self)
		btn.resize(btn.sizeHint())
		btn.move(50,100)
	
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.addQuitButton()
	ex.addButtonWithName('Please')
	ex.show()
	sys.exit(app.exec_())

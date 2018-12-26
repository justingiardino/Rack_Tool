#!/usr/bin/python3

#Create a quit button

import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication

class Example(QWidget):
    
	def __init__(self):
		
		super().__init__()
		
		self.initUI()
        
        
	def initUI(self):
	
		#create a quit button, still just a pushbutton object
		qbtn = QPushButton('Quit', self)
		#part of event processing system of PyQt5
		qbtn.clicked.connect(QApplication.instance().quit)
        #button size and location
		qbtn.resize(qbtn.sizeHint())
		#move to x location by y location
		qbtn.move(50, 50)       
		
		#Window size and location
		self.setGeometry(300, 600, 250, 150)
		self.setWindowTitle('Quit button')
        #self.show()
	
	def addButton(self):
		btn = QPushButton('Add', self)
		btn.resize(btn.sizeHint())
		btn.move(50,100)
        
        
if __name__ == '__main__':
    
	app = QApplication(sys.argv)
	ex = Example()
	ex.addButton()
	ex.show()
	sys.exit(app.exec_())
#!/usr/bin/python3

#Place two buttons in the bottom right corner

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QVBoxLayout


class Example(QWidget):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		#create two buttons
		okButton = QPushButton('OK')
		cancelButton = QPushButton('Cancel')
		
		#add a horizontal box layout
		hbox = QHBoxLayout()
		#add stretch factor - adds stretchable space before the two buttons. This pushes them to the far right
		hbox.addStretch(1)
		hbox.addWidget(okButton)
		hbox.addWidget(cancelButton)
		
		#create verticle box layout 
		vbox = QVBoxLayout()
		#add stretch factor to push buttons to bottom of screen
		vbox.addStretch(1)
		#place horizontal box inside verticle box
		vbox.addLayout(hbox)
		
		#set the layout of the main window
		self.setLayout(vbox)

		self.setGeometry(300,300, 250, 150)
		self.setWindowTitle('Absolute')
		

		
		
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

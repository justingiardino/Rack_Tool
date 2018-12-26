#!/usr/bin/python3

#Create a status bar

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication


class Example(QMainWindow):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		#create status bar and display a message
		self.statusBar().showMessage('Ready')
		
		self.setGeometry(300,300, 250, 150)
		self.setWindowTitle('Status Bar Window')
	
	
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

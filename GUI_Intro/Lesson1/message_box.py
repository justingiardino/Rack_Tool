#!/usr/bin/python3

#Create a quit button

import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication


class Example(QWidget):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		self.setGeometry(300,300,250,150)
		self.setWindowTitle('Message box')
	
	#closeEvent triggered when QWidget is closed
	def closeEvent(self, event):
	
		reply = QMessageBox.question(self, 'Warning', 'Are you sure to quit?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
		
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

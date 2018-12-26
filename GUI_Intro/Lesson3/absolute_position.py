#!/usr/bin/python3

#Create a layout using absolute positioning - not best practice
#This is the exact pixel location where something exists
#size and position of the widget will not change when you resize window 

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel


class Example(QWidget):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		#create a QLabel object
		lbl1 = QLabel('Zetcode', self)
		#move object to position x = 15, y = 10
		lbl1.move(15, 10)
		
		lbl2 = QLabel('tutorials', self)
		lbl2.move(35, 40)
		
		lbl3 = QLabel('for programmers', self)
		lbl3.move(55, 70)

		self.setGeometry(300,300, 250, 150)
		self.setWindowTitle('Absolute')
		

		
		
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

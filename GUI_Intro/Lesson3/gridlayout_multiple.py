#!/usr/bin/python3

#create skeleton of a calculator using grid layout

###
#This gridlayout could be useful for the rack layout

import sys
from PyQt5.QtWidgets import QWidget, QApplication,  QGridLayout, QLabel, QLineEdit, QTextEdit


class Example(QWidget):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		title = QLabel('Title')
		author = QLabel('Author')
		review = QLabel('Review')
		
		titleEdit = QLineEdit()
		authorEdit = QLineEdit()
		#Note that this one is a text edit instead of line
		reviewEdit = QTextEdit()
		
		grid = QGridLayout()
		grid.setSpacing(10)
		
		grid.addWidget(title, 1, 0)
		grid.addWidget(titleEdit, 1, 1)
		
		grid.addWidget(author, 2, 0)
		grid.addWidget(authorEdit, 2, 1)
		
		grid.addWidget(review, 3, 0)
		grid.addWidget(reviewEdit, 3, 1)
		
		self.setLayout(grid)

		self.setGeometry(300,300, 250, 150)
		self.setWindowTitle('Complex Layout')

		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

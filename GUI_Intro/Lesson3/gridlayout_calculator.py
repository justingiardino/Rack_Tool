#!/usr/bin/python3

#create skeleton of a calculator using grid layout

###
#This gridlayout could be useful for the rack layout

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QGridLayout


class Example(QWidget):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		#create grid object 
		grid = QGridLayout()
		#set the layout of the main window to be the layout of the grid
		self.setLayout(grid)
		
		#labels for buttons
		names = ['Cls', 'Bck', '', 'Close', '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '=', '+']
		
		#list of positions in the grid
		positions = [(i,j) for i in range(5) for j in range(4)]
		#returns [(0,0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), .. (4, 1), (4, 2), (4, 3)]
		#print(positions)
		
		#create buttons and add them to the layout as widgets
		for position, name in zip(positions, names):
			if name == '':
				continue
			button = QPushButton(name)
			grid.addWidget(button, *position)
		

		self.move(300, 150)
		self.setWindowTitle('Calculator')

		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

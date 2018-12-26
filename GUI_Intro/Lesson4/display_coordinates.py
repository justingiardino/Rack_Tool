#!/usr/bin/python3

#display x and y coordinates of mouse
#using event objects

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel

class Example(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		grid = QGridLayout()
		x = 0
		y = 0

		#format string as text
		self.text = "x: {0}, y: {1}".format(x,y)
		#set string as label box in display
		self.label = QLabel(self.text, self)
		#add label to top left of screen
		grid.addWidget(self.label, 0, 0, Qt.AlignTop)
		#enable tracking on mouse
		self.setMouseTracking(True)
		#set layout as grid
		self.setLayout(grid)

		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('Tracker')

	#this must be a built in function because when I spelled it wrong nothing happened so the name isn't just a label
	#e is the event object, it contains the data of the event that happened as the function was triggered
	def mouseMoveEvent(self, e):

		x = e.x()
		y = e.y()
		text = "x: {0}, y: {1}".format(x,y)
		self.label.setText(text)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

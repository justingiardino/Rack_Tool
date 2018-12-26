#!/usr/bin/python3

#Create a submenu flyout option

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QPushButton


class Example(QMainWindow):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		#create and display status bar in bottom left of screen
		self.statusbar = self.statusBar()
		#Set default value for status bar
		self.statusbar.showMessage('Ready')
		
		#create menu bar object
		menubar = self.menuBar()
		
		#create view menu for menu bar 
		viewMenu = menubar.addMenu('View')
		
		#use option checkable to create checkable menu 
		viewStatAct = QAction('View status bar', self, checkable=True)
		viewStatAct.setStatusTip('View status bar tip')
		#set status bar as visible from the start 
		viewStatAct.setChecked(True)
		
		#function that is called when the action takes place
		#calls toggleMenu which is defined below
		viewStatAct.triggered.connect(self.toggleMenu)
		
		#Add action to view menu
		viewMenu.addAction(viewStatAct)
				
		self.setGeometry(300,300, 250, 150)
		self.setWindowTitle('Submenu Window')
		
	def toggleMenu(self, state):
		
		if state:
			self.statusbar.show()
		else:
			self.statusbar.hide()
			
			
		

		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

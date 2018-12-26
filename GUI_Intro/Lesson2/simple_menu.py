#!/usr/bin/python3

#Create a status bar

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QAction
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		#create action object with icon and label
		exitAct = QAction(QIcon('exit.png'), '&Exit', self)
		#define keyboard shortcut
		exitAct.setShortcut('Ctrl+Q')
		#Similar to tool tip
		exitAct.setStatusTip('Exit app')
		#Action that takes place when action is triggered
		exitAct.triggered.connect(qApp.quit)
		
		#create status bar
		self.statusBar()
		
		#create a menu bar object
		menubar = self.menuBar()
		
		#create menu item on menu bar named file 
		fileMenu = menubar.addMenu('&File')
		
		#add action object 
		fileMenu.addAction(exitAct)

		
		self.setGeometry(300,300, 250, 150)
		self.setWindowTitle('Status Bar Window')
		

		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

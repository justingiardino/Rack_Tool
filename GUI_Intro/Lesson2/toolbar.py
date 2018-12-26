#!/usr/bin/python3

#Create a pop up menu when right clicking

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QAction
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		#create action object with label icon and shortcut
		exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.triggered.connect(qApp.quit)
		
		#create toolbar
		self.toolbar = self.addToolBar('Exit')
		self.toolbar.addAction(exitAct)

		self.setGeometry(300,300, 250, 150)
		self.setWindowTitle('Context Menu')
		
		
		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

#!/usr/bin/python3

#Create a skeleton for a classic GUI app with a menu bar, tool bar, status bar, and central widget

import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QApplication, QAction
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
	
		#creates a text editing widget
		textEdit = QTextEdit()
		#becomes the center widget of the main window
		self.setCentralWidget(textEdit)
		
		#create action object with label icon and shortcut
		exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(self.close)
		
		#create a status bar
		self.statusBar()
		
		#create menu bar, add File menu, add exit action to File menu
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAct)
		
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

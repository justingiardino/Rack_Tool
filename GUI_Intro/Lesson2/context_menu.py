#!/usr/bin/python3

#Create a pop up menu when right clicking

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QMenu


class Example(QMainWindow):
    
	def __init__(self):
		super().__init__()
		self.initUI()
		
	def initUI(self):
		
		self.setGeometry(300,300, 250, 150)
		self.setWindowTitle('Context Menu')
		
	def contextMenuEvent(self, event):
		
		cmenu = QMenu(self)
		
		newAct = cmenu.addAction('New')
		opnAct = cmenu.addAction('Open')
		quitAct = cmenu.addAction('Quit')
		#context menu is displayed when exec_ happens
		action = cmenu.exec_(self.mapToGlobal(event.pos()))
		
		#return value from context menu
		if action == quitAct:
			qApp.quit()
			
		

		
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

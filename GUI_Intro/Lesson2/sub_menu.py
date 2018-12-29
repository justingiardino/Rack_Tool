#!/usr/bin/python3

#Create a submenu flyout option

#A menu is a "top level" menu item
#Action is a "Second level" item
#A menu can be an action, this would be a submenu like a flyout

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QAction


class Example(QMainWindow):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):

		#create a menu bar object
		menubar = self.menuBar()

		#Create Menu item
		fileMenu = menubar.addMenu('File')

		#Create sub menu menu
		impMenu = QMenu('Import', self)
		#Create sub menu action
		impAct = QAction('Import mail', self)
		#Add action to submenu label
		impMenu.addAction(impAct)

		#Action is a top level menu item only, no submenus
		newAct = QAction('New', self)

		### Test adding extra menus and submenus
		editMenu = menubar.addMenu('Edit')
		editAct1 = QAction('Undo', self)
		editAct2 = QAction('Redo', self)
		editMenu.addAction(editAct1)
		editMenu.addAction(editAct2)
		editSub = QMenu('Clear', self)
		editSubAct1 = QAction('Clear Last Addition', self)
		editSubAct2 = QAction('Clear All', self)
		editSub.addAction(editSubAct1)
		editSub.addAction(editSubAct2)
		editMenu.addMenu(editSub)
		### End here

		#Add top level action item
		fileMenu.addAction(newAct)

		#Add submenu object, which includes the flyout option
		fileMenu.addMenu(impMenu)


		self.setGeometry(300,300, 250, 150)
		self.setWindowTitle('Submenu Window')



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

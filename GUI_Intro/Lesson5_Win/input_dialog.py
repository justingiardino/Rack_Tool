#!/usr/bin/python3

#simple signal and slot mechanisms
#signal is emitted when a particular event occurs
#slot is called when signal is emitted


import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QInputDialog, QApplication

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		
		self.btn = QPushButton('Dialog', self)
		self.btn.move(20,20)
		self.btn.clicked.connect(self.showDialog)
		
		self.le = QLineEdit(self)
		self.le.move(130,22)
		

		self.setGeometry(300, 300, 290, 150)
		self.setWindowTitle('Input Dialog')
		
		
	def showDialog(self):
		text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name: ')
		
		#ok is a boolean that is returned by input dialog
		if ok:
			#set line edit box text equal to 
			self.le.setText(str(text))

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

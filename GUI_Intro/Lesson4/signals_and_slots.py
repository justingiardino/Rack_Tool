#!/usr/bin/python3

#simple signal and slot mechanisms
#signal is emitted when a particular event occurs
#slot is called when signal is emitted


import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLCDNumber, QSlider, QVBoxLayout

class Example(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		lcd = QLCDNumber(self)
		sld = QSlider(Qt.Horizontal, self)

		vbox = QVBoxLayout()
		vbox.addWidget(lcd)
		vbox.addWidget(sld)

		self.setLayout(vbox)
		sld.valueChanged.connect(lcd.display)

		self.setGeometry(300, 300, 250, 150)
		self.setWindowTitle('Slider')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())

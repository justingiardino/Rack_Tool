#!/usr/bin/python3

#Change user input box to color


import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFontDialog, QSizePolicy, QVBoxLayout, QLabel
from PyQt5.QtGui import QColor

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()
        btn = QPushButton('Dialog', self)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.move(20, 20)

        vbox.addWidget(btn)

        btn.clicked.connect(self.showDialog)

        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(130,20)
        vbox.addWidget(self.lbl)

        self.setLayout(vbox)

        self.setGeometry(300,300, 250, 180)
        self.setWindowTitle('Color Dialog')

    def showDialog(self):

        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

#!/usr/bin/python3

#User choice from list of options
#this coudl be good for removing a device from the rack, that way the user can only select one

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QApplication

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.lbl = QLabel('Ubuntu', self)

        combo = QComboBox(self)
        combo.addItem('Ubuntu')
        combo.addItem('Mandriva')
        combo.addItem('Fedora')
        combo.addItem('Arch')
        combo.addItem('Gentoo')

        combo.move(50, 50)
        self.lbl.move(50,150)

        #when an item from the combo box is selected, signal is emitted
        combo.activated[str].connect(self.onActivated)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Combo')

    def onActivated(self, text):
        #set label text to new choice
        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

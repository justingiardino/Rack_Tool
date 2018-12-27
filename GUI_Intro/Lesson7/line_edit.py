#!/usr/bin/python3

#Show text entered in QLineEdit box, includes functinos that are included with QLineEdit


import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #create label object for displaying text
        self.lbl = QLabel(self)
        #create line edit object for inputting text
        qle = QLineEdit(self)

        #put line edit object below label
        qle.move(60, 100)
        self.lbl.move(60, 40)

        #connect signal that is emitted when the text is changed with the function onChanged
        qle.textChanged[str].connect(self.onChanged)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Line Edit Box')

    #when signal emitted connects to this function, the label is updated with the text in the text box
    def onChanged(self, text):

        self.lbl.setText(text)
        self.lbl.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

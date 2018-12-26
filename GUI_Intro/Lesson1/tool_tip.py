#!/usr/bin/python3



import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication
from PyQt5.QtGui import QFont    


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        
        QToolTip.setFont(QFont('SansSerif', 10))
        
        #can use RTF tags
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        #create push button object
        btn = QPushButton('Button', self)
        #set tip for button
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        #resize to suggested size
        btn.resize(btn.sizeHint())
        #move button to this pixel location
        btn.move(50, 50)       
        
        #set size and location of window
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Button Window')    
        
        #self.show()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
	#call show in main
    ex.show()
    sys.exit(app.exec_())
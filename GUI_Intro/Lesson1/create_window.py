#!/usr/bin/python3

#Create a window titled simple

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    
    app = QApplication(sys.argv)

    #create widget object with no parameters, creating a window
    w = QWidget()
    #set width and height
    w.resize(250, 150)
    #starting px values
    w.move(300, 300)
    w.setWindowTitle('Simple')
    #display
    w.show()
    
    sys.exit(app.exec_())
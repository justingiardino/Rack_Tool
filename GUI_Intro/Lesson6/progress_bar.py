#!/usr/bin/python3

#Display a timer and progress bar


import sys
from PyQt5.QtWidgets import QWidget, QProgressBar, QPushButton, QApplication
from PyQt5.QtCore import QBasicTimer

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        #use progress bar constructor
        self.pbar = QProgressBar(self)
        #set location and size, this creates a horizontal rectangle
        self.pbar.setGeometry(30, 40, 200, 25)

        #create button
        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        #connect signal of the button to our doAction function
        self.btn.clicked.connect(self.doAction)

        #create a timer object to be used with progress bar
        self.timer = QBasicTimer()
        self.step = 0

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Progress Bar')

    #Every QObject has a timerEvent handler, we are re-creating it for our needs
    def timerEvent(self, e):

        #when timer reaches 100 we need to stop the timer
        if self.step >= 100:
            #stop timer will also stop progress bar
            self.timer.stop()
            self.btn.setText('Finished')
            self.step = 0
            return

        #increment value on progress bar
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    #when button is clicked we are either stopping the timer or starting it
    def doAction(self):

        #if the timer is already running then the button should stop running
        if self.timer.isActive():
            self.timer.stop()
            #set message to say start since the progress bar is no longer going
            self.btn.setText('Start')

        #start timer object when timer is not running and button is clicked
        else:
            #start parameters are timeout period and object that receives the event
            self.timer.start(100, self)
            self.btn.setText('Stop')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

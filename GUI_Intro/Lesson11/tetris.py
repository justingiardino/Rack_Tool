#!/usr/bin/python3

#create a simple tetris game

#4 classes
#1 Tetris - setup game
#2 Board - Game logic
#Tetrominoe - names for all pieces
#Shape - code for shape of piece

#Using QtCore.QBasicTimer() to create game cycle
#draw a tetrominoe
#move shapes on a square by square basis
#create a mathematical board that is just a list of numbers


import sys, random
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QFrame
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal

class Tetris(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    #build app UI
    def initUI(self):

        #create board object and set to center of main window
        self.tboard = Board(Self)
        self.setCentralWidget(self.tboard)

        #create status bar for displaying messages
        self.statusbar = self.statusBar()
        #this uses a custom signal implemented in the board class
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        #initiate the game
        self.tboard.start()

        self.resize(180,380)
        self.center()
        self.setWindowTitle('Tetris')
        self.show()

    def center(self):

        screen = QDesktopWidget.screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,(screen.height()-size.height())/2)

class Board(QFrame):

    #create custom signal, signal is emitted when we want to write a message or the score to the status bar
    msg2Statusbar = pyqtSignal(str)

    #create variables for board size and speed, every 300ms a new game cycle starts
    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):

        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        #declare important variables
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        #board is a list of numbers from 0 to 7 for positions of various shapes on the boards
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

    #continue with shapeAt


if __name__ == '__main__':
    app = QApplication([]])
    tetris = Tetris()
    sys.exit(app.exec_())

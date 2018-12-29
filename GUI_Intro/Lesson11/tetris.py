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

    #determine shape at board position
    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

    #assign shape at board position
    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.BoardWidth) + x] = shape

    #board can be dynamically changed in size
    #determine width of one square
    def squareWidth(self):
        return self.contentsRect().width()

    #determine height
    def squareHeight(self):
        return self.contentsRect().height()

    #start game
    def start(self):

        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        #emit custom signal
        self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.newPiece()
        self.timer.start(Board.speed, self)

    #pause/unpause game
    def pause(self):

        if not self.isStarted:
            return

        #invert pause
        self.isPaused = not self.isPaused

        #pause
        if self.isPaused:
            self.timer.stop()
            #emit custom signal
            self.msg2Statusbar.emit('Pause')

        #unpause
        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

        self.update()

    #paint all shapes in game
    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

        #2d array
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)

                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter, rect.left() + j * self.squareWidth(), boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoe.NoShape:

            for i in range(4):

                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(), boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(), self.curPiece.shape())

    def keyPressEvent(self, event):

        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)

        key = event()

        #press p to pause game
        if key == Qt.Key_P:
            self.pause()
            return

        #if the game already is paused do nothing on arrow push
        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            #should use something like trymove for rack check
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        #down arrow rotates the piece right
        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)
        #up arrow rotates the piece left
        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)

    #left off on tiemr event 



if __name__ == '__main__':
    app = QApplication([]])
    tetris = Tetris()
    sys.exit(app.exec_())

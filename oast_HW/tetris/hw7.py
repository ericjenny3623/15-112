#################################################
# hw7.py: Tetris!
#
# Your name: Eric Jenny
# Your andrew id: ejenny
#
# Your partner's name: Jonny Notts
# Your partner's andrew id: jnotting
#################################################

import decimal
import cs112_f19_week7_linter
import math
import copy
import random

from cmu_112_graphics import *
from tkinter import *


#################################################
# model
#################################################

def playTetris():
    """ Called by main() function. Calls runApp after getting window dims
    """
    rows, cols, cellSize, margin = gameDimensions()
    x = margin*2 + cols*cellSize
    y = margin*2 + rows*cellSize
    print('Replace this with your Tetris game!')
    runApp(width=x, height=y)


def appStarted(app):
    """ Called by runApp() and by the tetris game upon reset ('r').
    Initiates values of the game.
    """
    app.boardColor = "blue"
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.pieceRow, app.pieceCol = 0, 0
    app.board = [[app.boardColor for i in range(app.cols)] \
                    for j in range(app.rows)]
    app.shapes, app.colors = tetrisPieces()
    app.piece, app.pieceColor = [], None
    newTetrisPiece(app)
    app.gameOver = False
    app.score = 0
    app.count = 0
    app.slowFactor = 1


def gameDimensions():
    """ Stores the values for rows, cols, cell size, and the margin of the
    board. Returns the 4 values in a tuple of corresponding order. Fake oop :(
    """
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return rows, cols, cellSize, margin


def tetrisPieces():
    """ Stores the shapes of tetris pieces and corresponding colors and returns
    each list. A shape is defined as a 2D list with each element shape[row][col]
    a boolean True if the shape exists in that grid element.
    """
    # Seven "standard" pieces (tetrominoes)
    iPiece = [
        [True,  True,  True,  True]
    ]
    jPiece = [
        [True, False, False],
        [True,  True,  True]
    ]
    lPiece = [
        [False, False,  True],
        [True,  True,  True]
    ]
    oPiece = [
        [True,  True],
        [True,  True]
    ]
    sPiece = [
        [False,  True,  True],
        [True,  True, False]
    ]
    tPiece = [
        [False,  True, False],
        [True,  True,  True]
    ]
    zPiece = [
        [True,  True, False],
        [False,  True,  True]
    ]
    tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    tetrisPieceColors = ["red", "yellow", "magenta",
                         "pink", "cyan", "green", "orange"]
    return tetrisPieces, tetrisPieceColors


#################################################
# view
#################################################

def redrawAll(app, canvas):
    """ Called periodically by the running app. Wrapper function which calls
    various sub-draw functions.
    """
    drawBoard(app, canvas)
    drawPiece(app, canvas)
    drawScore(app, canvas)
    if app.gameOver:
        drawGameOver(app, canvas)


def drawBoard(app, canvas):
    """ Draws the board by looping through app.board which is a 2D list storing
    the color values for each cell given by app.board[row][col].
    """
    canvas.create_rectangle(0, 0, app.width, app.height, fill="yellow")
    for col in range(app.cols):
        for row in range(app.rows):
            drawCell(app, canvas, row, col, app.board[row][col])


def drawPiece(app, canvas):
    """ Draws piece by looping over app.piece and calling drawCell for the
    current color if the current element in app.piece is True. Pieces row
    and col are offset by app.pieceRow and app.pieceCol which keep track
    of position.
    """
    piece, color = app.piece, app.color
    for row in range(len(piece)):
        for col in range(len(piece[0])):
            if piece[row][col]:
                drawCell(app, canvas, row+app.pieceRow,
                         col+app.pieceCol, color)


def drawCell(app, canvas, row, col, color):
    """ Lower level function which draws an individual cell.
    """
    x1, y1, x2, y2 = getCellCoords(row, col, app.margin, app.cellSize)
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=2)


def getCellCoords(row, col, margin, cellSize):
    """ Returns x1, y1, x2, y2, the coordinates of a cell in pixels given the
    cells row and column position according to the grid. 0, 0 (row, col) is top
    left.
    - Currently only called by helper function drawCell but could be used for
    other features such as using mouse to align piece.
    """
    x1 = margin + col*cellSize
    y1 = margin + row*cellSize
    x2 = x1 + cellSize
    y2 = y1 + cellSize
    return x1, y1, x2, y2


def drawScore(app, canvas):
    """ Draws the score at the top of the board, centered in the margin.
    """
    scoreText = f"Score: {app.score}"
    canvas.create_text(app.width/2, app.margin*0.5,
                           text=scoreText, fill="purple",
                           anchor="center")


def drawGameOver(app, canvas):
    """ Draws a black rectangle over board to indicate game over.
    """
    canvas.create_rectangle(0, app.height*0.2,
                        app.width, app.height*0.4,
                        fill="black")
    canvas.create_text(app.width/2, app.height*0.3,
                   text="GAME OVER", fill="yellow",
                   anchor="center")


#################################################
# controller
#################################################

def timerFired(app):
    """ Called periodically. Moves piece down at certain intervals and
    checks if the down move is illegal. If so, the piece has hit the
    bottom and is placed. At this point, another piece is generated and
    checked immediately. If this piece is illegal at the top of the board,
    the game is over. If not, the game continues.
    Also checks and clears any rows.
    """
    if app.gameOver:
        return

    if app.count % app.slowFactor == 0:
        if not movePiece(app, 1, 0):
            placePiece(app)
            checkRows(app)
            newTetrisPiece(app)
            if not pieceLegal(app):
                app.gameOver = True

    app.count += 1


def keyPressed(app, event):
    """ Called when a key is pressed. Responds to user input to move piece
    and reset game.
    """
    key = event.key
    if not app.gameOver:
        if key == "Down":
            movePiece(app, 1, 0)
        elif key == "Left":
            movePiece(app, 0, -1)
        elif key == "Right":
            movePiece(app, 0, 1)
        elif key == "Up":
            rotatePiece(app)
        elif key == "Space":
            dropPiece(app)

    if key == "r":
        appStarted(app)


def placePiece(app):
    """ Sets the falling piece in the board by overwriting the color of the
    board cell (app.board[row][col]) with the color of the piece.
    """
    piece, color = app.piece, app.color
    for row in range(len(piece)):
        for col in range(len(piece[0])):
            if piece[row][col]:
                app.board[row+app.pieceRow][col+app.pieceCol] = color


def checkRows(app):
    """ Checks all rows to see if they are full of non-board colors and
    removes that row if it is full adding a new row at the top of the board.
    """
    for row in app.board:
        if all(cell != app.boardColor for cell in row):
            app.board.remove(row)
            app.score += 1
            app.board.insert(0, [app.boardColor for i in range(app.cols)])


def newTetrisPiece(app):
    """ Sets the app.piece and app.pieceColor to a new piece given by the shape
    and color at a randomly generated index. Called at game start and when a
    piece is placed.
    """
    rand = random.randint(0, len(app.shapes) - 1)
    app.piece = app.shapes[rand]
    app.color = app.colors[rand]
    app.pieceRow = 0
    app.pieceCol = int(app.cols/2 - math.ceil(len(app.piece[0])/2))


def movePiece(app, drow, dcol):
    """ Moves a piece by incrementing app.pieceRow and app.pieceCol and checks
    if the piece is at a legal position. If illegal, resets the move.
    """
    app.pieceRow += drow
    app.pieceCol += dcol
    if not pieceLegal(app):
        app.pieceRow -= drow
        app.pieceCol -= dcol
        return False
    return True


def rotatePiece(app):
    """ Rotates the piece 90 degrees ccw by swapping rows and cols.
    The rows are essentially inversed first to acheive the ccw direction.
    The new piece is then shifted according to the center of the piece.
    If the piece at new orientation and position is in an illegal position,
    the operation is undone.
    """
    oldPiece = copy.copy(app.piece)
    rotatedPiece = []
    for i in range(len(app.piece[0])-1, -1, -1):
        rotatedPiece.append([app.piece[j][i] for j in range(len(app.piece))])
    app.piece = rotatedPiece
    app.pieceRow += len(app.piece)//2 - len(app.piece[0])//2

    if not pieceLegal(app):
        app.pieceRow -= len(app.piece)//2 - len(app.piece[0])//2
        app.piece = oldPiece


def dropPiece(app):
    """ Lowers the piece until the piece can no longer be lowered legally.
    """
    while movePiece(app, 1, 0):
        None


def pieceLegal(app):
    """ Checks if a piece is in a legal position and returns False if not.
    Checks if piece is off-board to left, right, or bottom and checks if any
    section of the shape is overlapping a cell on the board which has the fill
    color.
    """
    piece = app.piece
    for row in range(len(piece)):
        for col in range(len(piece[0])):
            boardRow = row+app.pieceRow
            boardCol = col+app.pieceCol
            if boardRow < 0 or boardRow >= app.rows:
                return False
            elif boardCol < 0 or boardCol >= app.cols:
                return False
            if piece[row][col] \
               and app.board[boardRow][boardCol] != app.boardColor:
                return False
    return True


#################################################
# main
#################################################

def main():
    cs112_f19_week7_linter.lint()
    playTetris()


if __name__ == '__main__':
    main()

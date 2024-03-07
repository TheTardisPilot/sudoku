from cs1graphics import *
from random import *
from sys import setrecursionlimit

import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

brown = (100,70,0)
green = (20,100,40)
black = (0,0,0)
grey = (200, 200, 200)
white = (255,255,255)

windowHeight = screensize[1]/2
windowWidth = screensize[0]/2

window = Canvas(windowWidth, windowHeight, black, "Sudoku Game", True)

numGrids = 9

gridSize = windowHeight/numGrids

# Grid is a list of the square graphic, point, column number, and row number
grid = list()
gridX = list()
gridY = list()
gridNums = list()

for i in range(numGrids**2):
    # Rather clever row and column assignment starting at index 0 for both.
    columnNum = i % numGrids
    rowNum = i // numGrids
    # Record X and Y
    gridX.append(int((columnNum * gridSize) + (gridSize / 2)))
    gridY.append(int((rowNum * gridSize) + (gridSize / 2)))
    # New square at X and Y
    newSquare = Square(gridSize, Point(gridX[i],gridY[i]))
    if (rowNum + columnNum) % 2 == 0:
        # Set grey color for even sum
        newSquare.setFillColor(grey)
    else:
        # Set white color for odd sum
        newSquare.setFillColor(white)
    # Add square to the grid list
    grid.append((newSquare,Point(gridX[i],gridY[i]), columnNum + 1, rowNum + 1))
    # Add the value of the grid, 0 means empty.
    number = Text("", 35, grid[i][1])
    # Store the text object, the location, the column, and the row.
    gridNums.append((number,grid[i][1], grid[i][2], grid[i][3]))
    # Render Changes
    window.add(newSquare)
    window.add(number)

gridLines = [Rectangle(3, windowHeight, Point(windowHeight/3, windowHeight/2)), Rectangle(3, windowHeight, Point((2*windowHeight)/3, windowHeight/2)), Rectangle(windowHeight, 3, Point(windowHeight/2, windowHeight/3)), Rectangle(windowHeight, 3, Point(windowHeight/2, (2*windowHeight)/3))]
for gridLine in gridLines:
    gridLine.setFillColor(black)
    gridLine.setBorderColor(black)
    gridLine.setBorderWidth(3)
    window.add(gridLine)

# Record gridNums into squares, columns, and rows for the sudoku game checks.
# Reminder: gridNums has number graphic(0), point(1), column number(2), and row number(3) in a list.
    
# This is a grid of 3x3 squares, each square is 3x3. So this means fourDim[squareColumn][squareRow][columnNum][rowNum]
fourDim = []
for i in range(3):
    threeDim = []
    for j in range(3):
        twoDim = []
        for k in range(3):
            oneDim = []
            for l in range(3):
                oneDim.append([])
            twoDim.append(oneDim)
        threeDim.append(twoDim)
    fourDim.append(threeDim)
for gridNum in gridNums:
    fourDim[(gridNum[2] - 1) // 3][(gridNum[3] - 1) // 3][(gridNum[2] - 1) % 3][(gridNum[3] - 1) % 3] = gridNum

help = None
helpBox1 = Text("", 20, Point(12*gridSize, 2*gridSize))
helpBox2 = Text("", 20, Point(12*gridSize, 2.5*gridSize))
helpBox1.setFontColor(white)
helpBox2.setFontColor(white)
window.add(helpBox1)
window.add(helpBox2)

# Given a rowNum, returns a list of unused numbers in the row.
def unusedRowNumbers(rowNum):
    usedNumbers = list()
    for gridNum in gridNums:
        message = gridNum[0].getMessage()
        if (gridNum[3] == rowNum) and message.isdigit() and message != "":
            usedNumbers.append(int(gridNum[0].getMessage()))
    # Since we have the numbers used, find which are not.
    unusedNumbers = [1,2,3,4,5,6,7,8,9]
    for num in usedNumbers:
        if num in unusedNumbers:
            unusedNumbers.remove(num)
    return unusedNumbers

# Given a columnNum, returns a list of unused numbers in the column.
def unusedColumnNumbers(columnNum):
    usedNumbers = list()
    for gridNum in gridNums:
        message = gridNum[0].getMessage()
        if (gridNum[2] == columnNum) and message.isdigit() and message != "":
            usedNumbers.append(int(gridNum[0].getMessage()))
    # Since we have the numbers used, find which are not.
    unusedNumbers = [1,2,3,4,5,6,7,8,9]
    for num in usedNumbers:
        if num in unusedNumbers:
            unusedNumbers.remove(num)
    return unusedNumbers

# Given a square (2dim list), returns a list of unused numbers in the square.
# The twodim list would be something like fourDim[1][1], which would be the twoDim[columnNum][rowNum]
def unusedSquareNumbers(twoDimSquare):
    usedNumbers = list()
    for column in twoDimSquare:
        for gridNum in column:
            message = gridNum[0].getMessage()
            if message.isdigit() and message != "":
                usedNumbers.append(int(message))
    # Since we have the numbers used, find which are not.
    unusedNumbers = [1,2,3,4,5,6,7,8,9]
    for num in usedNumbers:
        if num in unusedNumbers:
            unusedNumbers.remove(num)
    return unusedNumbers

# Given a gridNum, return a list of all possible replacements for that number
def possibleNumbers(gridIndex):
    unusedRowNums = unusedRowNumbers(gridNums[gridIndex][3])
    unusedColumnNums = unusedColumnNumbers(gridNums[gridIndex][2])
    twoDimSquare = fourDim[(gridNums[gridIndex][2] - 1) // 3][(gridNums[gridIndex][3] - 1) // 3]
    unusedSquareNums = unusedSquareNumbers(twoDimSquare)
    possibleNums = list(set(unusedSquareNums).intersection(list(set(unusedRowNums).intersection(unusedColumnNums))))
    return possibleNums

def isValidBoard():
    for i in range(numGrids**2):
        if len(possibleNumbers(i)) > 0:
            return False
    return True

def resetBoard():
    for i in range(numGrids**2):
        gridNums[i][0].setMessage("")

# Grid has tuple (square graphic, point, columnNum, rowNum)
def assignNumber(inputNum, gridIndex):
    # put text of number in box and record number for checking later.]
    if inputNum == "0":
        inputNum = ""
    gridNums[gridIndex][0].setMessage(str(inputNum))

# Given an event, checks mouse location and returns the grid's index for later use, returns None otherwise
def checkLocation(event):
    location = event.getMouseLocation()
    mCX = location.getX()
    mCY = location.getY()
    tolerance = int(gridSize / 2)
    for i in range(len(grid)):
        leftX = grid[i][1].getX() - tolerance
        rightX = grid[i][1].getX() + tolerance
        lowY = grid[i][1].getY() - tolerance
        topY = grid[i][1].getY() + tolerance
        if (leftX <= mCX) and (mCX <= rightX) and (lowY <= mCY) and (mCY <= topY):
            return i
    return None

# By randomly plugging in acceptable numbers, hopefully solve the puzzle. Totally efficient and doesn't have to rely on luck or anything.
setrecursionlimit(2000)
x = 0
copy = list()
def solve():
    global x
    global copy
    x += 1
    helpBox1.setMessage(f"Solve attempt {x}")
    helpBox2.setMessage("")
    if x == 1:
        copy = [gridNum[0].getMessage() for gridNum in gridNums]
    try:
        for i in range(len(gridNums)):
            message = gridNums[i][0].getMessage()
            if message == "":
                possible = possibleNumbers(i)
                if possible:
                    randomNum = choice(possible)
                    assignNumber(randomNum, i)
                else:
                    raise IndexError
        helpBox1.setMessage(f"Solved in {x} tries!")
        helpBox2.setMessage("")
        x = 0
    except IndexError as e:
        print(e)
        for i, gridNum in enumerate(gridNums):
            gridNum[0].setMessage(copy[i])
        solve()


# Add controls instructions
instructions = Text("Press ' for autosolve, press ; to see if board is solved, press / to reset board \nEscape to exit (when box not selected)\nTo insert, click on a box and (required) press a number next.", 10, Point(12.5*gridSize, 0.5*gridSize))
instructions.setFontColor(white)
window.add(instructions)

# Run game until exit
exit = False
while not exit:
    action = window.wait()
    print("description is", action.getDescription())
    # debug
    if(action.getDescription() == "keyboard"):
        print("debug", action.getKey())
    elif "mouse click" == action.getDescription():
        gridIndex = checkLocation(action)
        if gridIndex != None:
            gridClicked = grid[gridIndex][1]
            print("debug, click is on grid ", gridClicked)
            helpBox1.setMessage("This box can have: ")
            helpBox2.setMessage(str(possibleNumbers(gridIndex)))
            inputNum = "hi"
            while not inputNum.isnumeric():
                print("Grid clicked, Choose 0 to delete.")
                action2 = window.wait()
                inputNum = action2.getKey()
            print(f"Num is {inputNum}")
            assignNumber(inputNum, gridIndex)
    else:
        print("debug", action.getDescription())
    # Check exit
    if(action.getKey() == chr(27)):
        exit = True
    elif(action.getKey() == "'"):
        solve()
    elif(action.getKey() == ";"):
        if isValidBoard():
            helpBox1.setMessage("This board is valid!")
            helpBox2.setMessage("YAY!")
        else:
            helpBox1.setMessage("This board is not valid.")
            helpBox2.setMessage("You stink")
    elif(action.getKey() == "/"):
        resetBoard()
window.close()

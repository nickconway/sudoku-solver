# Choices
QUIT = "q"
SOLVE_SAVE = "s"
PLAY = "p"
UNDO = "u"
YES = "y"
NO = "n"
YES_NO = [YES, NO]

# Strings
PLAY_SOLVE = "Do you want to play (p), or solve (s)? "
PLAY_SAVE = "Do you want to play (p), save (s), undo (u), or quit (q)? "
GOODBYE = "Good bye! Here is the final board:"
INCORRECT = " does not belong in position "
NO_UNDO = "There are no more moves to undo!"
UNDONE = "The move was undone at position "
WON = "You won!"
INVALID_CHOICE = "Please enter a vallid choice!"
CORRECTNESS = "Do you want to check for correctness (y or n)? "
INVALID_ROW = "Please enter a valid row (1 - 9)!"
INVALID_COL = "Please enter a valid column (1 - 9)!"
INVALID_NUM = "Please enter a valid number (1 - 9)!"
WON = "You won!"
NO_WIN = "You filled the board, but didn't win."
VIOLATES_ROW = "That row already contains a"
VIOLATES_COL = "That column already contains a"
VIOLATES_SQUARE = "That square already contains a"
FILLED = "That space is already filled!"
SOLVING = "Getting solution..."


# Spaces
BLANK = 0


# prettyPrint() prints the board with row and column labels,
#               and spaces the board out so that it looks nice
# Input:        board;   the square 2d game board (of integers) to print
# Output:       None;    prints the board in a pretty way
def prettyPrint(board):
	# print column headings and top border
	print("\n    1 2 3 | 4 5 6 | 7 8 9 ") 
	print("  +-------+-------+-------+")

	for i in range(len(board)): 
		# convert "0" cells to underscores  (DEEP COPY!!!)
		boardRow = list(board[i]) 
		for j in range(len(boardRow)):
			if boardRow[j] == 0:
				boardRow[j] = "_"

		# fill in the row with the numbers from the board
		print( "{} | {} {} {} | {} {} {} | {} {} {} |".format(i + 1, 
				boardRow[0], boardRow[1], boardRow[2], 
				boardRow[3], boardRow[4], boardRow[5], 
				boardRow[6], boardRow[7], boardRow[8]) )

		# the middle and last borders of the board
		if (i + 1) % 3 == 0:
			print("  +-------+-------+-------+")




# savePuzzle() writes the contents a sudoku puzzle out
#              to a file in comma separated format
# Input:       board;    the square 2d puzzle (of integers) to write to a file
#              fileName; the name of the file to use for writing to 
def savePuzzle(board, fileName):
	ofp = open(fileName, "w")
	for i in range(len(board)):
		rowStr = ""
		for j in range(len(board[i])):
			rowStr += str(board[i][j]) + ","
		# don't write the last comma to the file
		ofp.write(rowStr[ : len(rowStr)-1] + "\n")
	ofp.close()





# initializeGame() initializes all necessary variables
# Input: fileName, the file name to get the board from
# output: a list of the initial board, solved board, and the moves
def initializeGame(fileName):
	# make all the initial values
	board = makeBoard(fileName)
	prettyPrint(board)
	print(SOLVING)
	# solve the board
	solvedBoard = solve(board)
	moves = []
	return [board, solvedBoard, moves]




# makeBoard() creates the initial board from the file
# Input: fileName, the name of the file to read from
# output: initialBoard, the list that represents the initial board
def makeBoard(fileName):
	# open the file for reading the board
	initialBoard = []
	data = open(fileName, "r")

	# go through each row and add it to the board list
	for row in data:
		newRow = []
		# remove commas
		for number in row.split(","):
			newRow.append(int(number))

		initialBoard.append(newRow[:])

	data.close()
	return initialBoard



# getExcludedNumbers() gets the numbers to compare the desired number to 
# Input: board, the board
#        row, the row to compare to
#        col, the column to compare to 
# Output: toCheck, a list of all the numbers to compare
def getExcludedNumbers(board, row, col):
	# Initialize lists 
	toCheck = []
	# create the row the space is in
	row_ = board[row]
	column = []
	square = []
	
	# create the column the space is in
	for number in range(9):
		column.append(board[number][col])


	# create the square the space is in
	startingRow = (row // 3) * 3
	startingCol = (col // 3) * 3
	for rowNum in range(startingRow, (startingRow + 3)):
		for colNum in range(startingCol, (startingCol + 3)):
			square.append(board[rowNum][colNum])

	# add all the numbers to a list to check the rules
	for num in row_:
		toCheck.append(num)
	for num in column:
		toCheck.append(num)
	for num in square:
		toCheck.append(num)
	
	return toCheck


# solve() solves the game given a board
# Input: board, the list representing the board
# output: solvedBoard, the solved board
def solve(board):
	
	# make a shallow copy of the rows in the board so they are not changed
	solvedBoard = []
	for row in board:
		solvedBoard.append(row[:])

	# Check every blank space
	for row in range(9):
		for col in range(9):
			if board[row][col] == BLANK:
				for number in range(1, 10):
					# Only check numbers that don't validate the rules
					toCheck = getExcludedNumbers(solvedBoard, row, col)
					if number not in toCheck:
						solvedBoard[row][col] = number
						# solve the rest of the board
						tempBoard = solve(solvedBoard)
						if tempBoard:
							return tempBoard
				# go back and try again with a new number
				return False

	return solvedBoard




# getChoice() gets the users choice and validates it
# Input: options, the options the player has to choose from (list)
# output: choice, the users choice
def getChoice(options):
	# after the user has chosen to play or solve
	if QUIT in options:
		# get the choice and validate
		choice =  input(PLAY_SAVE)
		while choice not in options:
			print(INVALID_CHOICE)
			choice =  input(PLAY_SAVE)
	# initial choice to play or solve
	else:
		# get the choice and validate
		choice = input(PLAY_SOLVE)
		while choice not in options:
			print(INVALID_CHOICE)
			choice =  input(PLAY_SOLVE)

	return choice



# isBoardFull() checks if the board is full
# Input: board, the list representing the board
# output: True or False
def isBoardFull(board):
	# check every item in the board and see if there are any blank spaces
	for row in board:
		if BLANK in row:
			return False
	return True





# correctnessCheck() checks if the user wants to check for correctness
# Input: None
# output: True or False
def correctnessCheck():
	# see if user wants to check for correctness and validate
	toCheck = input(CORRECTNESS)
	while toCheck not in YES_NO:
		print(INVALID_CHOICE)
		toCheck = input(CORRECTNESS)

	# return boolean
	return True if toCheck == YES else False




# undoMove() undoes the last move
# Input: moves, the list of moves 
#        board, the board to undo the move on 
# output: a list containing the new board after the undo, and the moves
def undoMove(moves, board):
	# when the user hasn't made a move yet
	if len(moves) == 0:
		print(NO_UNDO)
		return [moves, board]

	# Let the user know the move was undone
	print("The " + \
	str(board[moves[len(moves) - 1][0]][moves[len(moves) - 1][1]]) + \
	" was removed from position (" + \
	str(moves[len(moves) - 1][0] + 1) + ", " + \
	str(moves[len(moves) - 1][1] + 1) + ")")

	# make the space blank, update the moves list and return 
	board[moves[len(moves) - 1][0]][moves[len(moves) - 1][1]] = BLANK
	moves = moves[:len(moves) - 1]
	return [moves, board]




# getMove() gets the users choice and validates it
# Input: board, the board being played on 
# output: a list containing the row, column, and number to play
def getMove(board):
	# get the row number and validate
	row = int(input("What row do you want to put a number in (1 - 9)? ")) - 1
	while (row) not in range(9):
		print(INVALID_ROW)
		row = int(input("What row do you want to put a number in (1 - 9)? ")) - 1

	# get the column number and validate
	col = int(input("What column do you want to put a number in (1 - 9)? ")) - 1
	while (col) not in range(9):
		print(INVALID_COL)
		col = int(input("What column do you want to put a number in (1 - 9)? ")) - 1

	# get the number to play and validate
	number = int(input("What number do you want to play (1 - 9)? "))
	while number not in range(1, 10):
		print(INVALID_NUM)
		number = int(input("What number do you want to play (1 - 9)? "))

	# this is entered when the user enters a number that is invalid in some way
	while board[row][col] != BLANK or number in getExcludedNumbers(board, row, col):
		# return a blank space when the desired space is filled
		if board[row][col] != BLANK:
			print(FILLED)
			return [row, col, BLANK]
		# return the number when it violates one of the 3 rules
		elif number in getExcludedNumbers(board, row, col):
			return [row, col, number]

		# get all the desired values again
		row = int(input("What row do you want to put a number in (1 - 9)? "))
		row -= 1
		while (row) not in range(9) and board[row][col] != BLANK:
			print(INVALID_ROW)
			row = int(input("What row do you want to " + \
			"put a number in (1 - 9)? "))
			row -= 1

		col = int(input("What column do you want to " + \
		"put a number in (1 - 9)? "))
		col -= 1
		while (col) not in range(9):
			print(INVALID_COL)
			col = int(input("What column do you want to " + \
			"put a number in (1 - 9)? "))
			col -= 1

		number = int(input("What number do you want to play (1 - 9)? "))
		while number not in range(1, 10):
			print(INVALID_NUM)
			number = int(input("What number do you want to play (1 - 9)? "))

	# list to return 
	return [row, col, number]
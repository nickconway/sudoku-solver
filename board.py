import pygame
class Board():
	def __init__(self):
		self.initializeBoard()
		self.moves = []

	# prettyPrint() prints the board with row and column labels,
	#               and spaces the board out so that it looks nice
	# Input:        board;   the square 2d game board (of integers) to print
	# Output:       None;    prints the board in a pretty way
	def prettyPrint(self, solved = False):

		toPrint = self.spaces if not solved else self.solved

		# print column headings and top border
		print("\n    1 2 3 | 4 5 6 | 7 8 9 ") 
		print("  +-------+-------+-------+")

		for i in range(len(toPrint)): 
			# convert "0" cells to underscores  (DEEP COPY!!!)
			boardRow = list(toPrint[i]) 
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

	# initializeBoard() creates the initial board from the file
	# Input: fileName, the name of the file to read from
	# output: initialBoard, the list that represents the initial board
	def initializeBoard(self):

		# open the file for reading the board
		fileName = "puzzle.txt"
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

		self.spaces = initialBoard
		self.prettyPrint()

		print("Getting solution...")
		self.solved = self.solve(self.spaces)

	# solve() solves the game given a board
	# Input: board, the list representing the board
	# output: solvedBoard, the solved board
	def solve(self, board):
		
		# make a shallow copy of the rows in the board so they are not changed
		solvedBoard = []
		for row in board:
			solvedBoard.append(row[:])

		# Check every blank space
		for row in range(9):
			for col in range(9):
				if board[row][col] == 0:
					for number in range(1, 10):
						# Only check numbers that don't validate the rules
						toCheck = self.getExcludedNumbers(solvedBoard, row, col)
						if number not in toCheck:
							solvedBoard[row][col] = number
							# solve the rest of the board
							tempBoard = self.solve(solvedBoard)
							if tempBoard:
								return tempBoard
					# go back and try again with a new number
					return False

		self.solved = solvedBoard
		return solvedBoard


	# getExcludedNumbers() gets the numbers to compare the desired number to 
	# Input: board, the board
	#        row, the row to compare to
	#        col, the column to compare to 
	# Output: toCheck, a list of all the numbers to compare
	def getExcludedNumbers(self, board, row, col):
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

	# isBoardFull() checks if the board is full
	# Input: board, the list representing the board
	# output: True or False
	def isBoardFull(self):
		# check every item in the board and see if there are any blank spaces
		for row in self.spaces:
			if 0 in row:
				return False
		return True

	# undoMove() undoes the last move
	# Input: moves, the list of moves 
	#        board, the board to undo the move on 
	# output: a list containing the new board after the undo, and the moves
	def undoMove(self):
		
		# when the user hasn't made a move yet
		if len(self.moves) == 0:
			print("There are no more moves to undo!")
			return 

		# Let the user know the move was undone
		number = str(self.spaces[self.moves[0][0]][self.moves[0][1]])
		print("The " + number + " was removed from position (" + str(self.moves[len(self.moves) - 1][0] + 1) + ", " + str(self.moves[len(self.moves) - 1][1] + 1) + ")")

		# make the space blank, update the moves list and return 
		self.spaces[self.moves[len(self.moves) - 1][0]][self.moves[len(self.moves) - 1][1]] = 0
		self.moves = self.moves[:len(self.moves) - 1]
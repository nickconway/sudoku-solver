import sys
from board import Board

class Game:
	def __init__(self):
		self.board = Board()
		self.correctnessCheck()
		self.solved = False

	# savePuzzle() writes the contents a sudoku puzzle out
	#              to a file in comma separated format
	# Input:       board;    the square 2d puzzle (of integers) to write to a file
	#              fileName; the name of the file to use for writing to 
	def savePuzzle(self):
		fileName = input("Enter the file name to save under: ")
		filePath = open(fileName, "w")

		for i in range(len(self.board.spaces)):
			rowStr = ""
			for j in range(len(self.board.spaces[i])):
				rowStr += str(self.board.spaces[i][j]) + ","
			# don't write the last comma to the file
			filePath.write(rowStr[ : len(rowStr)-1] + "\n")

		filePath.close()

	# getChoice() gets the users choice and validates it
	# Input: options, the options the player has to choose from (list)
	# output: choice, the users choice
	def getChoice(self, options):
		# after the user has chosen to play or solve
		if "q" in options:
			# get the choice and validate
			choice =  input("Do you want to play (p), save (s), undo (u), or quit (q)? ")
			while choice not in options:
				print("Please enter a valid choice!")
				choice =  input("Do you want to play (p), save (s), undo (u), or quit (q)? ")
		# initial choice to play or solve
		else:
			# get the choice and validate
			choice = input("Do you want to play (p), or solve (s)? ")
			while choice not in options:
				print("Please enter a valid choice!")
				choice =  input("Do you want to play (p), or solve (s)? ")

		return choice

	# correctnessCheck() checks if the user wants to check for correctness
	# Input: None
	# output: True or False
	def correctnessCheck(self):
		# see if user wants to check for correctness and validate
		toCheck = input("Do you want to check for correctness (y or n)? ")
		while toCheck not in ["y", "n"]:
			print("Please enter a vallid choice!")
			toCheck = input("Do you want to check for correctness (y or n)? ")

		# return boolean
		self.correctness = True if toCheck == "y" else False

	# getMove() gets the users choice and validates it
	# Input: board, the board being played on 
	# output: a list containing the row, column, and number to play
	def getMove(self):
		# get the row number and validate
		row = self.getRow()
		col = self.getCol()
		num = self.getNum()

		# list to return 
		return row, col, num

	def getRow(self):
		# get the row number and validate
		row = int(input("What row do you want to put a number in (1 - 9)? ")) - 1
		while (row) not in range(9):
			print("Please enter a valid row (1 - 9)!")
			row = int(input("What row do you want to put a number in (1 - 9)? ")) - 1

		return row

	def getCol(self):
		# get the col number and validate
		col = int(input("What column do you want to put a number in (1 - 9)? ")) - 1
		while (col) not in range(9):
			print("Please enter a valid column (1 - 9)!")
			col = int(input("What column do you want to put a number in (1 - 9)? ")) - 1

		return col

	def getNum(self):
		# get the number and validate
		num = int(input("What number do you want to put a number in (1 - 9)? "))
		while (num) not in range(10):
			print("Please enter a valid number (1 - 9)!")
			num = int(input("What number do you want to put a number in (1 - 9)? "))

		return num

	def makeMove(self):
		# Get the move from the user
		row, col, num = self.getMove()
		movePosition = [row, col]

		# Check for correctness
		if self.correctness:
			if num == self.board.solved[row][col]:
				# Make the move and update the move list
				self.board.spaces[row][col] = num
				self.board.moves.append(movePosition)
			else:
				print(str(num) + " does not belong in position (" + str(row+ 1) + ", " + str(col + 1) + ")")
		# when not checking for correctness
		else:
			# when the desired space is not empty
			if self.board.spaces[row][col] == 0:
				# Tell the user if they are violating the 3 rules
				if num in self.board.getExcludedNumbers(self.board.spaces, row, col):
					print(str(num) + " cannot go here")
				else:
					# Make the move and update the move list
					self.board.spaces[row][col] = num
					self.board.moves.append(movePosition)

	def play(self):
		userChoice = self.getChoice(["p", "s"])

		# Solve the board
		if userChoice == "s":
			self.board.prettyPrint(True)
			self.solved = True

		if userChoice == "p":
			# Checks if the user wants to check for correctness
			self.correctnessCheck()

			# Keep playing until the board is full or the user quits
			while (not self.board.isBoardFull()):
				self.board.prettyPrint()

				# Get userChoice from user
				userChoice = self.getChoice(["p", "s", "u", "q"])

				# If the user wants to play
				if userChoice == "p":
					self.makeMove()

				# save the game
				if userChoice == "s":
					self.savePuzzle()

				# undo the last move
				if userChoice == "u":
					self.board.undoMove()

				# quit the game
				if userChoice == "q":
					sys.exit()

		# tell the user if they won or not
		if not self.solved:
			self.board.prettyPrint()
			if self.board.spaces == self.board.solved:
				print("You won!")
			elif self.board.isBoardFull(self.board.spaces):
				print("You filled the board, but didn't win.")

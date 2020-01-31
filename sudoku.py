# SUDOKU
# THIS PROJECT LOADS A SUDOKU BOARD FROM A TEXT FILE AND ALLOWS THE USER
# TO ATTEMPT TO SOLVE THE PUZZLE, OR TO AUTOMATICALLY SOLVE IT AT ANY
# GIVEN TIME DURING THE GAME. THE USER CAN ALSO SAVE THE GAME AND
# RESUME AT ANY TIME

import sys
import pygame
from pygame.locals import *
from imports import *

def main():

	# Initialize board and other necessities
	pygame.init()
	screen = pygame.display.set_mode([800, 800])
	fileName = input("Enter the filename: ")
	initial = initializeGame(fileName)
	board = initial[0]
	solvedBoard = initial[1]
	moves = initial[2]
	solved = False
	userChoice = getChoice([PLAY, SOLVE_SAVE])

	# Solve the board
	if userChoice == SOLVE_SAVE:
		prettyPrint(solvedBoard)
		solved = True

	if userChoice == PLAY:
		# Checks if the user wants to check for correctness
		correctness = correctnessCheck()

		# Keep playing until the board is full or the user quits
		while (not isBoardFull(board)) and userChoice != QUIT:
			prettyPrint(board)
			# Get userChoice from user
			userChoice = getChoice([PLAY, SOLVE_SAVE, UNDO, QUIT])

			# If the user wants to play
			if userChoice == PLAY:
				# Get the move from the user
				move = getMove(board)
				row = move[0]
				col = move[1]
				num = move[2]
				movePosition = [row, col]

				# Check for correctness
				if correctness:
					if num == solvedBoard[row][col]:
						# Tell the user if they are violating the 3 rules
						if num in getExcludedNumbers(board, row, col):
							if num in getExcludedNumbers(board, row, col)[:9]:
								print(VIOLATES_ROW, str(num) + ".")
							if num in getExcludedNumbers(board, row, col)[9:18]:
								print(VIOLATES_COL, str(num) + ".")
							if num in getExcludedNumbers(board, row, col)[18:27]:
								print(VIOLATES_SQUARE, str(num) + ".")
						else:
							# Make the move and update the move list
							board[row][col] = num
							moves.append(movePosition)
					else:
						print(str(num) + INCORRECT + "(" + \
						str(row+ 1) + ", " + \
						str(col + 1) + ")")

				# when not checking for correctness
				else:
					# when the desired space is not empty
					if num != BLANK:
						# Tell the user if they are violating the 3 rules
						if num in getExcludedNumbers(board, row, col):
							if num in getExcludedNumbers(board, row, col)[:9]:
								print(VIOLATES_ROW, str(num) + ".")
							if num in getExcludedNumbers(board, row, col)[9:18]:
								print(VIOLATES_COL, str(num) + ".")
							if num in getExcludedNumbers(board, row, col)[18:27]:
								print(VIOLATES_SQUARE, str(num) + ".")
						else:
							# Make the move and update the move list
							board[row][col] = num
							moves.append(movePosition)

			# save the game
			if userChoice == SOLVE_SAVE:
				fileName = input("Enter the file name to save under: ")

				savePuzzle(board, fileName)

			# undo the last move
			if userChoice == UNDO:
				undone = undoMove(moves, board)
				moves = undone[0]
				board = undone[1]

			# quit the game
			if userChoice == QUIT:
				print(GOODBYE)

	# tell the user if they won or not
	if not solved:
		prettyPrint(board)
		if board == solvedBoard:
			print(WON)
		elif isBoardFull(board):
			print(NO_WIN)

main()

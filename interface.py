import tkinter as tk
from tkinter import tix
import sys
from game import Game

class Interface:
	def __init__(self):
		self.game = Game()
		# self.game.play()
		self.window = tix.Tk(className="Sudoku")
		self.window.title("Sudoku")

		buttons = tk.Frame(self.window)
		fileButton = tk.tix.FileEntry(buttons, label="Choose file: ", command=self.makeBoard).pack(side="left")
		solveButton = tk.Button(buttons, width=25, text="Solve", command=self.solvePuzzle).pack(side="left")
		saveButton = tk.Button(buttons, width=25, text="Save", command=self.game.savePuzzle).pack(side="left")
		buttons.pack()

		self.window.mainloop()
		self.game.board.prettyPrint(True)

	def solvePuzzle(self):
		grid = tk.Frame(self.window)
		for i in range(9):
			for j in range(9):
				value = tk.Label(grid, text=str(self.game.board.solved[i][j]), width=2).grid(row=i, column=j)
			grid.pack()

	def makeBoard(self, fileName):
		self.game.board.initializeBoard(fileName)
		grid = tk.Frame(self.window)
		self.configurators = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0]
		]

		if(self.game.board.spaces):
			for i in range(9):
				for j in range(9):
					if self.game.board.spaces[i][j] == 0:
						textInput = tk.Entry(grid, width=2)
						textInput.grid(row=i, column=j)
						self.configurators[i][j] = textInput
					else:
						value = tk.Label(grid, text=str(self.game.board.spaces[i][j]), width=2).grid(row=i, column=j)
			grid.pack()

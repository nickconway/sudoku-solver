import pygame, sys
from pygame.locals import *
from pygame_functions import *
from game import Game

class Interface:
	def __init__(self):
		pygame.init()
		self.drawWindow()
		self.game = Game()
		# self.game.play()
		self.update()

	def drawWindow(self):
		self.width = 800
		self.window = pygame.display.set_mode((self.width, self.width))
		pygame.display.set_caption("Sudoku - Nick Conway")
		icon = pygame.image.load("images/icon.png")
		pygame.display.set_icon(icon)

	def drawLines(self):
		gap = self.width / 9
		for i in range(10):
			if i % 3 == 0 and i != 0:
				width = 5
			else:
				width = 1
			pygame.draw.line(self.window, (255,255,255), (0, i * gap), (self.width, i * gap), width)
			pygame.draw.line(self.window, (255,255,255), (i * gap, 0), (i * gap, self.width), width)

	def update(self):
		while True:
			self.window.fill((0, 0, 0))
			self.drawLines()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						self.game.makeMove()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_s:
						self.game.savePuzzle()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.game.board.spaces = self.game.board.solve(self.game.board.spaces)

			font = pygame.font.Font("Rajdhani-Bold.ttf", 32)
			for i in range(9):
				for j in range(9):

					if(self.game.board.spaces[i][j] == 0):
						textBox = makeTextBox((self.width / 9 * j + (self.width / 9 / 2) - 8), (self.width / 9 * i + (self.width / 9 / 2) - 16), self.width / 9, case=0, startingText=str(self.game.board.spaces[i][j]), maxLength=0, fontSize=32)
						showTextBox(textBox)
						entry = textBoxInput(textBox)
					else:
						toRender = str(self.game.board.spaces[i][j])
						text = font.render(toRender, True, (255,255,255))
						self.window.blit(text, (self.width / 9 * j + (self.width / 9 / 2) - 8, self.width / 9 * i + (self.width / 9 / 2) - 16))
					# toRender = "" if self.game.board.spaces[i][j] == 0 else str(self.game.board.spaces[i][j])
					# text = font.render(toRender, True, (255,255,255))
					# self.window.blit(text, (self.width / 9 * j + (self.width / 9 / 2) - 8, self.width / 9 * i + (self.width / 9 / 2) - 16))

			pygame.display.update()
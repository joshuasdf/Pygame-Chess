import pygame
import chess
import chess.variant

from piece import Piece

pygame.init()
pygame.font.init()
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN])


class Chessgame:
	def __init__(self):
		self.board_length = 600
		self.screen = pygame.display.set_mode(
			(self.board_length, self.board_length), pygame.DOUBLEBUF)
		
		self.gamemode = None

		self.run = 1
		self.length = self.board_length // 8
		self.selected_piece = None
		self.check = None
		self.color = 'w'

		# self.chessboard = chess.Board("4k2r/8/8/8/8/8/8/4K3")
		self.chessboard = chess.Board()

		self.coordinates = [
			["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
			["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
			["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
			["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
			["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
			["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
			["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
			["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"],
		]

		self.board = [
			['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
			['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
			['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
		]


	def cord(self, pos):
		return pos[0]//self.length, pos[1]//self.length

	def get_board(self):
		chess_pieces = {'r': 'br','n': 'bn','b': 'bb','q': 'bq','k': 'bk','p': 'bp','.': ' ','R': 'wr','N': 'wn','B': 'wb','Q': 'wq','K': 'wk','P': 'wp'}

		string = str(self.chessboard)
		result = [line.split(" ") for line in string.split("\n")]


		for i in range(8):
			for j in range(8):
				result[i][j] = chess_pieces[result[i][j]]

		self.board = result if self.color == 'w' else [sublist[::-1] for sublist in result[::-1]]

	def update(self):
		# font
		self.get_board()
		self.screen.fill((0, 0, 0))
		text = "white" if self.color == 'w' else 'black'
		opposite = "black" if text == "white" else "white"

		if self.chessboard.outcome() == None:
			turn_text = "Turn: "+text

		else:
			turn_text = opposite + " wins!" if self.chessboard.outcome().winner != None else "Draw!"
			self.run = 0

		pygame.display.set_caption("Chess | Gamemode: " + self.gamemode + " | "+turn_text)


		yellow = (255, 255, 0)

		self.screen.blit(pygame.transform.scale(pygame.image.load("assets/boards/chess_board1.png").convert(), (self.board_length, self.board_length)), (0, 0))

		if self.chessboard.is_check():
			self.check = self.color[0]
		else:
			self.check = None

		# for i in self.highlighted_squares:
		# 	x, y = i

		# 	a = pygame.Surface((self.length, self.length))
		# 	a.set_alpha(100)
		# 	a.fill(yellow)

		# 	self.screen.blit(a, (self.length*x, self.length*y))

		if self.selected_piece != None:
			a = pygame.Surface((self.length, self.length))
			a.set_alpha(100)
			a.fill(yellow)

			self.screen.blit(
				a, (self.selected_piece[0]*self.length, self.selected_piece[1]*self.length))

		for column in range(8):
			for row in range(8):

				if self.check != None:
					if self.board[column][row] == f'{self.check}k':
						pygame.draw.rect(
							self.screen, (255, 0, 0), (row*self.length, column*self.length, self.length, self.length))

				if self.board[column][row] != ' ':
					Piece().draw(self.screen, row, column,
									self.board[column][row], self.length)

	def next_turn(self):
		self.color = "w" if self.color == "b" else "b"

		# flip board
		for i in range(8):
			self.coordinates[i] = self.coordinates[i][::-1]

		self.coordinates = self.coordinates[::-1]

		self.selected_piece = None
		# self.highlighted_squares.clear()

	def loop(self):
		if self.gamemode == 'Classic':
			self.chessboard = chess.Board()
		elif self.gamemode == 'Atomic':
			self.chessboard = chess.variant.AtomicBoard()
		elif self.gamemode == 'Horde':
			self.chessboard = chess.variant.HordeBoard()

		self.screen = pygame.display.set_mode((self.board_length, self.board_length), pygame.DOUBLEBUF)
		
		self.update()
		pygame.display.update()

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					self.screen.fill((0,0,0))
					

				if event.type == pygame.MOUSEBUTTONDOWN:
					try:
						
						if self.run:
							x, y = self.cord(event.pos)

							if self.selected_piece == (x,y):
								self.selected_piece = None
								self.update()
								pygame.display.update()

							elif self.selected_piece != None:
		
								# self.highlighted_squares.clear()

								ax = self.selected_piece[0]
								ay = self.selected_piece[1]
								self.selected_piece = None

								clicked_coord = self.coordinates[ay][ax]
								move_to_coord = self.coordinates[y][x]


								move = chess.Move.from_uci(
									clicked_coord+move_to_coord)

								if (self.board[ay][ax] == 'wp' and clicked_coord[1] == '7' and move_to_coord[1] == '8') or (self.board[ay][ax] == 'bp' and clicked_coord[1] == '2' and move_to_coord[1] == '1'):
									move = chess.Move.from_uci(
										clicked_coord+move_to_coord+'q')

									self.next_turn()
									self.chessboard.push(move)

								elif self.chessboard.is_legal(move):
									self.next_turn()
									self.chessboard.push(move)
									
								else:
									self.selected_piece = None
									# self.highlighted_squares.clear()

							if self.board[y][x][0] == self.color:
								self.selected_piece = (x, y)if(
									self.selected_piece != (x, y)) else(None)

							self.update()

							Piece().kill()
							pygame.display.update()
					except Exception as e:
						print(e)

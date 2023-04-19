import pygame

from chessgame import Chessgame

pygame.init()
pygame.font.init()

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])

class ModeButtons(pygame.sprite.Sprite):
	def __init__(self, coord, dimensions):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(dimensions)
		self.rect.center = coord

class Mouse_Location(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,1,1)
	

class Gui:
	def __init__(self):
		self.chessgame = Chessgame()

		self.screen = pygame.display.set_mode(
			(self.chessgame.board_length, self.chessgame.board_length), pygame.DOUBLEBUF)

		self.length, self.width = self.screen.get_size()

		pygame.display.set_caption("Home")
		self.menu_phase = True

		self.modes = ['Classic', 'Atomic', 'Horde']
		self.rects = pygame.sprite.Group()

	def create_text(self, options):
		text_size = 50
		font = pygame.font.SysFont("arial", text_size-10)
		title_font = pygame.font.SysFont("arial", (text_size-10)*2)

		length_apart = self.width/(len(options)+1)

		text = title_font.render("Gamemodes", True, (0,0,0))
		text_rect = text.get_rect(center = (self.length/2,80))
		self.screen.blit(text,text_rect)

		for i in range(len(options)):

			y = (i+2)*length_apart-text_size-(length_apart/3)

			rect = ModeButtons((self.length/2, y), (50, 50, (len(options[i]))*(text_size/2), text_size))
			
			self.rects.add(rect)

			pygame.draw.rect(self.screen, (0,0,0), rect.rect)

			text = font.render(options[i], True, (200, 200, 200))
			text_rect = text.get_rect(center=(self.length/2, y))
			self.screen.blit(text, text_rect)

	def loop(self):
		self.screen.fill((200, 200, 200))
		self.create_text(self.modes)


		pygame.display.update()
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					break
				elif event.type == pygame.KEYDOWN:
					pass
				elif event.type == pygame.MOUSEBUTTONDOWN:
					pos = Mouse_Location(event.pos[0], event.pos[1])

					s = 0
					for i in self.rects:
						if pygame.sprite.collide_rect(i, pos):
							self.chessgame.gamemode = self.modes[s]
							self.menu_phase = False
						s += 1

					if not self.menu_phase:
						self.chessgame.loop()

					pygame.display.update()

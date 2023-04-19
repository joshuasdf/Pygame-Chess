import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def draw(self, screen, x, y, piece, distance):
        screen.blit(pygame.transform.scale(pygame.image.load(f"assets/{piece}.png").convert_alpha(), (distance, distance)), (x*distance, y*distance))
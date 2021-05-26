import pygame

from constants import *


class PowerUp:
    def __init__(self, x_pos, y_pos, type, image=None):
        self.x = x_pos
        self.y = y_pos

        self.i = int(self.y / square_length)
        self.j = int(self.x / square_length)

        self.type = type
        types = {'extraBombs': (120, 40, 140), 'powerIncrease': (255, 211, 0), 'extraLife': (0, 255, 255),
                 'door': (255, 255, 255)}

        self.color = types[self.type]

        self.validity = True
        self.sprite = image

    def touch(self, jugador):
        return abs(jugador.x - self.x) < square_length and abs(jugador.y - self.y) < square_length

    def used(self, jugador):
        if self.type != 'door':
            if self.type == 'extraBombs':
                jugador.maxBombs += 10
            elif self.type == 'powerIncrease':
                jugador.bombStrength += 1
            elif self.type == 'extraLife':
                jugador.lives += 1
            self.validity = False

    def draw(self, surface):
        if self.sprite is None:
            if self.type == 'door':
                square = [self.x - square_length / 2, self.y - square_length / 2, square_length, square_length]
                pygame.draw.rect(surface, self.color, square)
            else:
                pygame.draw.circle(surface, self.color, [int(self.x), int(self.y)], square_length / 2 - 5)
        else:
            surface.blit(self.sprite, (int(self.x) - square_length / 2, int(self.y) - square_length / 2))

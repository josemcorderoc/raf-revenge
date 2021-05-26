import pygame
from math import pi, sin, cos

from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glBegin, glVertex2f, glEnd, GL_POLYGON

from constants import BURNTIME, square_length


class Fire:
    def __init__(self, x_pos, y_pos, image=None):
        self.x = x_pos
        self.y = y_pos
        self.color = (255 / 255.0, 117 / 255.0, 20 / 255.0)
        self.startTime = pygame.time.get_ticks()
        self.duration = BURNTIME
        self.validity = True
        self.sprite = image

    def burn(self, object):
        """
        True si el fuego quema algún objeto, False si no
        :param object: Player, Policeman, Wall
        :return: boolean
        """
        if type(object).__name__ == "Player" and object.inmortal:  # si jugador es inmortal no es quemado
            return False
        return abs(object.x - self.x) < square_length and abs(object.y - self.y) < square_length

    def draw(self, surface):
        if self.sprite is None:
            R1 = square_length / 2
            R2 = R1 - 5
            glColor3f(*self.color)
            glBegin(GL_POLYGON)
            step = 36
            for angulo in range(0, 360, step):
                angulo = angulo * pi / 180
                step = step * pi / 180
                glVertex2f(self.x + R1 * cos(angulo), self.y + R1 * sin(angulo))
                glVertex2f(self.x + R2 * cos(angulo + step / 2), self.y + R2 * sin(angulo + step / 2))
            glEnd()
        else:
            surface.blit(self.sprite, (int(self.x) - square_length / 2, int(self.y) - square_length / 2))

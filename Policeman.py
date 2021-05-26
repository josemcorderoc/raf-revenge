import random

from OpenGL.GL import glBegin
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, GL_QUADS, glEnd, glVertex2f

from Player import Player
from constants import *


class Policeman(Player):
    def __init__(self, initial_x, initial_y, speed, image=None):
        Player.__init__(self, initial_x, initial_y, speed, image)

        self.color = (0, 0, 255)
        self.autoDirection = ''
        self.inertia = False

    def draw(self, surface):
        super(Policeman, self).draw(surface)
        if self.sprite is None:
            glColor3f(1, 1, 1)
            glBegin(GL_QUADS)
            glVertex2f(self.x - 7, self.y - square_length / 2)
            glVertex2f(self.x + 7, self.y - square_length / 2)
            glVertex2f(self.x + 7, self.y - square_length / 2 + 4)
            glVertex2f(self.x - 7, self.y - square_length / 2 + 4)
            glEnd()

    def touch(self, player):
        if not player.inmortal:
            return abs(player.x - self.x) < square_length - 12 and abs(player.y - self.y) < square_length

    def autoMove(self, city):
        # movimientos aleatorios
        if self.inertia:
            if self.traveledDistance == square_length:
                self.inertia = False
                self.autoDirection = ''
                self.traveledDistance = 0
            else:
                if square_length - self.traveledDistance < self.speed:
                    self.move(self.autoDirection, square_length - self.traveledDistance)
                else:
                    self.move(self.autoDirection)
        else:
            self.inertia = True
            directions = []
            if city[self.i + 1, self.j, 2] == 0:
                directions.append('y')
            if city[self.i - 1, self.j, 2] == 0:
                directions.append('-y')
            if city[self.i, self.j + 1, 2] == 0:
                directions.append('x')
            if city[self.i, self.j - 1, 2] == 0:
                directions.append('-x')

            if len(directions) > 0:
                self.autoDirection = random.choice(directions)
                self.move(self.autoDirection)

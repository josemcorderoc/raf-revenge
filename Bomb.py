import pygame
from OpenGL import *
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glVertex2f, GL_TRIANGLE_FAN, glEnd, glBegin

from constants import *
from Fire import Fire
from math import pi, sin, cos


class Bomb:
    def __init__(self, x_pos, y_pos, explosionTime, strength, image = None):
        self.x = x_pos
        self.y = y_pos

        self.i = int(self.y/square_length)
        self.j = int(self.x/square_length)
        self.startTime = pygame.time.get_ticks()
        self.endTime = None
        self.explosionTime = explosionTime
        self.strength = strength
        self.color = (0, 255, 0)
        self.validity = True
        self.sprite = image

        self.boom = pygame.mixer.Sound("Resources/explosion.wav")

        self.fuego = None
        if not OPENGLMODE:
            self.fuego = pygame.image.load("Resources/fuego.png")

    def explode(self, city, fireQueue):
        # dependiendo del tipo de la bomba y los muros cercanos, agregar fuego a la lista
        fireQueue.append(Fire(self.x, self.y, self.fuego))
        self.boom.play()

        # onda de bomba en Y
        for n in range(self.strength):
            y = city[self.i + n + 1, self.j, 0]
            x = city[self.i + n + 1, self.j, 1]
            if city[self.i + n + 1, self.j, 2] == -10:
                break
            elif city[self.i + n + 1, self.j, 2] == -5:
                fireQueue.append(Fire(x, y, self.fuego))
                break
            else:
                fireQueue.append(Fire(x, y, self.fuego))

        # onda de bomba en -Y
        for n in range(self.strength):
            y = city[self.i - n - 1, self.j, 0]
            x = city[self.i - n - 1, self.j, 1]
            if city[self.i - n - 1, self.j, 2] == -10:
                break
            elif city[self.i - n - 1, self.j, 2] == -5:
                fireQueue.append(Fire(x, y, self.fuego))
                break
            fireQueue.append(Fire(x, y, self.fuego))

        # onda de bomba en X
        for n in range(self.strength):
            y = city[self.i, self.j + n + 1, 0]
            x = city[self.i, self.j + n + 1, 1]
            if city[self.i, self.j + n + 1, 2] == -10:
                break
            elif city[self.i, self.j + n + 1, 2] == -5:
                fireQueue.append(Fire(x, y, self.fuego))
                break
            fireQueue.append(Fire(x, y, self.fuego))

        # onda de bomba en -X
        for n in range(self.strength):
            y = city[self.i, self.j - n - 1, 0]
            x = city[self.i, self.j - n - 1, 1]
            if city[self.i, self.j - n - 1, 2] == -10:
                break
            elif city[self.i, self.j - n - 1, 2] == -5:
                fireQueue.append(Fire(x, y, self.fuego))
                break
            fireQueue.append(Fire(x, y, self.fuego))

    def draw(self, surface):
        if self.sprite is None:
            R = square_length / 3
            a_head = 2 * pi / 10
            glColor3f(0.0, 1.0, 0.0)
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(self.x, self.y)
            for i in range(11):
                a = a_head * i
                glVertex2f(self.x + R * cos(a), self.y + R * sin(a))

            glEnd()
        else:
            surface.blit(self.sprite, (int(self.x) - square_length / 2, int(self.y) - square_length / 2))

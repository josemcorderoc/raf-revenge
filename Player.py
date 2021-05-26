import random
import pygame
from OpenGL.GL import glBegin
from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glVertex2f, GL_TRIANGLE_FAN, GL_QUADS, glEnd, GL_POLYGON
from constants import *
from Bomb import Bomb
from math import pi, sin, cos


class Player(object):
    def __init__(self, initial_x, initial_y, speed, image=None):

        # posición (en pixeles)
        self.x = initial_x
        self.y = initial_y
        # cuadrado correspondiente
        self.i = int(self.y / square_length)
        self.j = int(self.x / square_length)

        self.speed = speed
        self.bombStrength = 1
        self.alive = True
        self.color = (255, 0, 0)
        self.lives = LIVES

        self.traveledDistance = 0

        self.maxBombs = BOMBNUM
        self.placedBombs = 0

        self.inmortal = False
        self.inmortalTime = 0
        self.inmortalStart = 0

        self.sprite = image
        self.drop = pygame.mixer.Sound("Resources/dropgrenade.wav")

        self.bomb = None
        if not OPENGLMODE:
            self.bomb = pygame.image.load("Resources/grenade.png")

    def move(self, direction, distance=None):
        if not self.alive:
            return
        if distance is None:
            distance = self.speed
        if direction == 'x':
            self.x += distance
        elif direction == '-x':
            self.x -= distance
        elif direction == 'y':
            self.y += distance
        elif direction == '-y':
            self.y -= distance

        self.i = int(self.y / square_length)
        self.j = int(self.x / square_length)
        self.traveledDistance += distance

    def setInmortal(self, time):
        """
        vuelve al jugador inmortal por el tiempo señalado
        :param time: tiempo en segundos
        :return: None
        """
        self.inmortal = True
        self.inmortalTime = time
        self.inmortalStart = pygame.time.get_ticks()

    def setMortal(self):
        """
        vuelve al jugador mortal
        :return: None
        """
        self.inmortal = False
        self.inmortalTime = 0
        self.inmortalStart = 0

    def repeatLevel(self, city):
        """
        resetea al jugador en el mapa
        :return: None
        """
        emptySquares = []
        for i in range(1, y_squares - 1):
            for j in range(1, x_squares - 1):
                if city[i, j, 2] == 0:
                    emptySquares.append((i, j))
        random.shuffle(emptySquares)

        self.i = emptySquares[0][0]
        self.j = emptySquares[0][1]

        self.x = city[self.i, self.j, 1]
        self.y = city[self.i, self.j, 0]

        self.setInmortal(6)

    def placeBomb(self, city, bombQueue):
        """
        coloca bomba en posición del jugador
        :param playerNumber:
        :return:
        """
        if not self.alive:
            return
        if self.placedBombs < self.maxBombs and city[self.i, self.j, 2] not in [-10, -5,
                                                                                -44]:  # no se ha superado el maximo de bombas permitidas
            self.drop.play()
            # se aproxima la bomba al cuadrante vacío más cercano
            y = city[self.i, self.j, 0]
            x = city[self.i, self.j, 1]
            bombQueue.append(Bomb(x, y, BOMBTIME, self.bombStrength, self.bomb))
            city[self.i, self.j, 2] = -44
            self.placedBombs += 1

    def draw(self, surface):
        if not self.alive:
            return
        if self.inmortal:
            if (pygame.time.get_ticks() / 250) % 2 == 0:
                if self.sprite is None:
                    glColor3f(*SKIN_COLOR)
                    # cabeza
                    x_head = self.x
                    y_head = self.y - square_length / 6 - 6
                    r_head = square_length / 6
                    a_head = 2 * pi / 10
                    glBegin(GL_TRIANGLE_FAN)
                    glVertex2f(x_head, y_head)
                    for i in range(11):
                        a = a_head * i
                        glVertex2f(x_head + r_head * cos(a), y_head + r_head * sin(a))
                    glEnd()

                    # tronco
                    glColor3f(*self.color)
                    glBegin(GL_QUADS)
                    glVertex2f(self.x - 5, self.y - square_length / 6)
                    glVertex2f(self.x + 5, self.y - square_length / 6)
                    glVertex2f(self.x + 5, self.y + square_length / 4 - 3)
                    glVertex2f(self.x - 5, self.y + square_length / 4 - 3)
                    glEnd()

                    # brazos
                    glColor3f(*self.color)
                    manga = 4
                    glBegin(GL_POLYGON)  # brazo 1
                    glVertex2f(self.x - 5, self.y - square_length / 6)
                    glVertex2f(self.x - 5, self.y - square_length / 6 + manga + 2)
                    glVertex2f(self.x - 5 - 5, self.y - square_length / 6 + manga + 10)
                    glVertex2f(self.x - 5 - 5 - manga, self.y - square_length / 6 + manga + 10)
                    glEnd()

                    glBegin(GL_POLYGON)  # brazo 1
                    glVertex2f(self.x + 5, self.y - square_length / 6)
                    glVertex2f(self.x + 5, self.y - square_length / 6 + manga + 2)
                    glVertex2f(self.x + 5 + 5, self.y - square_length / 6 + manga + 10)
                    glVertex2f(self.x + 5 + 5 + manga, self.y - square_length / 6 + manga + 10)
                    glEnd()

                    # pantalones
                    glColor3f(0.0, 0.0, 0.0)
                    glBegin(GL_POLYGON)
                    glVertex2f(self.x - 5, self.y + square_length / 4 - 3)
                    glVertex2f(self.x + 5, self.y + square_length / 4 - 3)
                    glVertex2f(self.x + 6, self.y + square_length / 2)
                    glVertex2f(self.x + 2, self.y + square_length / 2)
                    glVertex2f(self.x, self.y + square_length / 4)
                    glVertex2f(self.x - 2, self.y + square_length / 2)
                    glVertex2f(self.x - 6, self.y + square_length / 2)
                    glEnd()
                else:
                    surface.blit(self.sprite, (int(self.x) - square_length / 2, int(self.y) - square_length / 2))
        else:
            if self.sprite is None:
                # pygame.draw.circle(surface, self.color, [int(self.x), int(self.y)], square_length / 2)
                glColor3f(*SKIN_COLOR)
                # cabeza
                x_head = self.x
                y_head = self.y - square_length / 6 - 6
                r_head = square_length / 6
                a_head = 2 * pi / 10
                glBegin(GL_TRIANGLE_FAN)
                glVertex2f(x_head, y_head)
                for i in range(11):
                    a = a_head * i
                    glVertex2f(x_head + r_head * cos(a), y_head + r_head * sin(a))
                glEnd()

                # tronco
                glColor3f(*self.color)
                glBegin(GL_QUADS)
                glVertex2f(self.x - 5, self.y - square_length / 6)
                glVertex2f(self.x + 5, self.y - square_length / 6)
                glVertex2f(self.x + 5, self.y + square_length / 4 - 3)
                glVertex2f(self.x - 5, self.y + square_length / 4 - 3)
                glEnd()

                # brazos
                glColor3f(*self.color)
                manga = 4
                glBegin(GL_POLYGON)  # brazo 1
                glVertex2f(self.x - 5, self.y - square_length / 6)
                glVertex2f(self.x - 5, self.y - square_length / 6 + manga + 2)
                glVertex2f(self.x - 5 - 5, self.y - square_length / 6 + manga + 10)
                glVertex2f(self.x - 5 - 5 - manga, self.y - square_length / 6 + manga + 10)
                glEnd()

                glBegin(GL_POLYGON)  # brazo 1
                glVertex2f(self.x + 5, self.y - square_length / 6)
                glVertex2f(self.x + 5, self.y - square_length / 6 + manga + 2)
                glVertex2f(self.x + 5 + 5, self.y - square_length / 6 + manga + 10)
                glVertex2f(self.x + 5 + 5 + manga, self.y - square_length / 6 + manga + 10)
                glEnd()

                # pantalones
                glColor3f(0.0, 0.0, 0.0)
                glBegin(GL_POLYGON)
                glVertex2f(self.x - 5, self.y + square_length / 4 - 3)
                glVertex2f(self.x + 5, self.y + square_length / 4 - 3)
                glVertex2f(self.x + 6, self.y + square_length / 2)
                glVertex2f(self.x + 2, self.y + square_length / 2)
                glVertex2f(self.x, self.y + square_length / 4)
                glVertex2f(self.x - 2, self.y + square_length / 2)
                glVertex2f(self.x - 6, self.y + square_length / 2)
                glEnd()
            else:
                surface.blit(self.sprite, (int(self.x) - square_length / 2, int(self.y) - square_length / 2))

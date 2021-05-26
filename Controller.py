import sys

import pygame
from OpenGL.raw.GL.VERSION.GL_1_0 import glMatrixMode, glLoadIdentity, glOrtho, glTranslatef, GL_PROJECTION
# from pygame.locals import *
from pygame import DOUBLEBUF, OPENGL

from constants import *
from Window import Window
from Player import Player
from Policeman import Policeman
from Wall import Wall
from PowerUp import PowerUp
import numpy as np
import random
from math import sqrt


class Controller:
    def __init__(self):

        # Constantes
        self.height = HEIGHT
        self.width = WIDTH

        self.bombNum = BOMBNUM
        self.bombStrength = STRENGTH

        # inicializar pygame y mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.init()
        if OPENGLMODE:
            self.screen = pygame.display.set_mode([self.width, self.height], DOUBLEBUF|OPENGL)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(0, self.width, self.height, 0, 0, 1)
            glTranslatef(0, 100, 0)
        else:
            self.screen = pygame.display.set_mode([self.width, self.height])
        pygame.display.set_caption('RAF Revenge')

        # recursos
        self.muroduro = None
        self.muroblando = None
        self.andreas = None
        self.andreasP2 = None
        self.germanpolice = None
        self.germansoldier = None
        self.fuego = None
        self.grenade = None
        self.powerUp_sprites = {'extraBombs': None, 'powerIncrease': None, 'extraLife': None,'door': None}

        if not OPENGLMODE:
            self.muroduro = pygame.image.load("Resources/hardwall.png")
            self.muroblando = pygame.image.load("Resources/softwall.png")
            self.andreas = pygame.image.load("Resources/andreas1.png")
            self.andreasP2 = pygame.image.load("Resources/andreasP2.png")
            self.germanpolice = pygame.image.load("Resources/paco.png")
            self.germansoldier = pygame.image.load("Resources/milico.png")
            self.fuego = pygame.image.load("Resources/fuego.png")
            self.powerUp_sprites['extraBombs'] = pygame.image.load("Resources/extraBombs.png")
            self.powerUp_sprites['powerIncrease' ] = pygame.image.load("Resources/powerIncrease.png")
            self.powerUp_sprites['extraLife'] = pygame.image.load("Resources/extraLife.png")

        # fuentes
        self.font = pygame.font.Font('Resources/Molot.otf', 25)
        self.font.set_underline(True)
        self.font2 = pygame.font.Font('Resources/Molot.otf', 35)
        self.font3 = pygame.font.Font('Resources/Molot.otf', 20)
        self.fonts = [self.font, self.font2, self.font3]

        # sonidos y música
        self.drop = pygame.mixer.Sound("Resources/dropgrenade.wav")
        pygame.mixer.music.load("Resources/soundtrack.wav")
        pygame.mixer.music.play(-1, 0.0)

        # multijugador
        self.multiplayer = MULTIPLAYER

        # inicializamos los modelos
        self.player = Player(0, 0, SPEED, self.andreas)
        self.players = [self.player]

        if self.multiplayer:  # características de multijugador
            self.player2 = Player(0, 0, SPEED, self.andreasP2)
            self.player.maxBombs = 25
            self.player2.maxBombs = 25
            self.players.append(self.player2)

        self.hardWalls = []
        self.softWalls = []
        self.bombs = []
        self.policemen = []
        self.powerUps = []
        self.fires = []

        self.city = np.zeros((y_squares, x_squares, 4))
        # k = 0,1: coordenadas; k = 2: muros; k = 3: powerUps/puerta/bombas
        # muro soft: -5, muro hard: -10, power up: -100, bomba: -44
        for i in range(y_squares):
            for j in range(x_squares):
                self.city[i, j, 0] = i * square_length + square_length / 2
                self.city[i, j, 1] = j * square_length + square_length / 2

        self.pausa = False
        self.score = 0
        self.currentTime = 0
        self.startTime = pygame.time.get_ticks()
        self.leftTime = GAMETIME

        self.window = Window(self.screen, self.players, self.softWalls, self.hardWalls, self.powerUps, self.policemen,
                             self.bombs, self.fires, self.fonts, self.startTime, self.score, self.multiplayer)


    def setScene(self):
        # colocar murallas duras
        for j in range(x_squares):
            # y = 0
            y = self.city[0, j, 0]
            x = self.city[0, j, 1]
            self.hardWalls.append(Wall(x, y, 'hard', self.muroduro))
            self.city[0, j, 2] = -10

            # y = y_squares
            y = self.city[y_squares - 1, j, 0]
            x = self.city[y_squares - 1, j, 1]
            self.hardWalls.append(Wall(x, y, 'hard', self.muroduro))
            self.city[y_squares - 1, j, 2] = -10

        for i in range(1, y_squares - 1):
            # x = 0
            y = self.city[i, 0, 0]
            x = self.city[i, 0, 1]
            self.hardWalls.append(Wall(x, y, 'hard', self.muroduro))
            self.city[i, 0, 2] = -10

            # x = x_squares
            y = self.city[i, x_squares - 1, 0]
            x = self.city[i, x_squares - 1, 1]
            self.hardWalls.append(Wall(x, y, 'hard', self.muroduro))
            self.city[i, x_squares - 1, 2] = -10

        # mallado de muros
        for i in range(2, y_squares - 1, 2):
            for j in range(2, x_squares - 1, 2):
                y = self.city[i, j, 0]
                x = self.city[i, j, 1]
                self.hardWalls.append(Wall(x, y, 'hard', self.muroduro))
                self.city[i, j, 2] = -10

        # lista auxiliar de cuadrados vacíos
        emptySquares = []
        for i in range(1, y_squares - 1):
            for j in range(1, x_squares - 1):
                if self.city[i, j, 2] == 0:
                    emptySquares.append((i, j))

        random.shuffle(emptySquares)

        # elegir aleatoriamente P+1/P+2 espacios vacíos (para colocar policías y jugador/es)

        # jugador
        self.player.i, self.player.j = emptySquares.pop(0)
        self.player.y = self.player.i * square_length + square_length / 2
        self.player.x = self.player.j * square_length + square_length / 2

        # jugador 2
        if self.multiplayer:
            self.player2.i, self.player2.j = emptySquares.pop(0)
            self.player2.y = self.player2.i * square_length + square_length / 2
            self.player2.x = self.player2.j * square_length + square_length / 2

        # dejamos despejado un cuadrante de radio 2 (para evitar que jugador parta encerrado)

        i_quadrant = random.choice([-1, 1])
        j_quadrant = random.choice([-1, 1])

        for k in range(len(emptySquares) - 1, -1, -1):
            cond_i = i_quadrant * (emptySquares[k][0] - self.player.i) <= 0 \
                     and abs(emptySquares[k][0] - self.player.i) <= 2
            cond_j = j_quadrant * (emptySquares[k][1] - self.player.j) <= 0 \
                     and abs(emptySquares[k][1] - self.player.j) <= 2

            cond_i_2 = False
            cond_j_2 = False

            if self.multiplayer:
                cond_i_2 = i_quadrant * (emptySquares[k][0] - self.player2.i) <= 0 \
                           and abs(emptySquares[k][0] - self.player2.i) <= 2
                cond_j_2 = j_quadrant * (emptySquares[k][1] - self.player2.j) <= 0 \
                           and abs(emptySquares[k][1] - self.player2.j) <= 2

            if (cond_i and cond_j) or (cond_i_2 and cond_j_2):
                emptySquares.pop(k)

        # Asegurarse que jugador/es y pacos queden mínimo a X distancia
        contEnemies = 0
        for k in range(len(emptySquares)):
            if contEnemies == NUMENEMIES: break
            farFromPlayer1 = abs(self.player.i - emptySquares[k][0]) > ENEMYDISTANCE \
                             or abs(self.player.j - emptySquares[k][1]) > ENEMYDISTANCE
            farFromPlayer2 = True

            if self.multiplayer:
                farFromPlayer2 = abs(self.player.i - emptySquares[k][0]) > ENEMYDISTANCE \
                                 or abs(self.player.j - emptySquares[k][1]) > ENEMYDISTANCE

            if farFromPlayer1 and farFromPlayer2:
                i_enemy, j_enemy = emptySquares.pop(k)
                y_enemy = i_enemy * square_length + square_length / 2
                x_enemy = j_enemy * square_length + square_length / 2
                if contEnemies < 2:
                    self.policemen.append(Policeman(x_enemy, y_enemy, SPEED / 2 + 1, self.germansoldier))
                else:
                    self.policemen.append(Policeman(x_enemy, y_enemy, SPEED / 2, self.germanpolice))
                contEnemies += 1

        # colocar murallas blandas (de forma aleatoria)
        numSoftWalls = random.randint(int(0.4 * len(emptySquares)), int(0.55 * len(emptySquares)))

        for i, j in random.sample(emptySquares, numSoftWalls):
            y = self.city[i, j, 0]
            x = self.city[i, j, 1]
            self.softWalls.append(Wall(x, y, 'soft', self.muroblando))
            self.city[i, j, 2] = -5

        # elegir aleatoriamente N+1 murallas blandas (para colocar debajo los N powerUps y la puerta)

        powerUpsAndDoor = random.sample(self.softWalls, NumPowerUps + 1)

        for k in range(NumPowerUps):
            x = powerUpsAndDoor[k].x
            y = powerUpsAndDoor[k].y
            if k % 3 == 0:
                type = 'extraBombs'
            elif k % 2 == 0:
                type = 'extraLife'
            else:
                type = 'powerIncrease'
            self.powerUps.append(PowerUp(x, y, type, self.powerUp_sprites[type]))
            i = int(y / square_length)
            j = int(x / square_length)
            self.city[i, j, 3] = -100

        x, y = powerUpsAndDoor[NumPowerUps].x, powerUpsAndDoor[NumPowerUps].y
        self.powerUps.append(PowerUp(x, y, 'door'))
        i = int(y / square_length)
        j = int(x / square_length)
        self.city[i, j, 3] = -100

    def update(self):
        self.window.clean()
        self.window.draw()

        # tiempo
        self.currentTime = pygame.time.get_ticks() - self.startTime
        self.leftTime = GAMETIME - self.currentTime - self.startTime
        self.window.leftTime = self.leftTime
        self.window.score = self.score
        if self.leftTime <= 0:
            self.player.lives = -1

        # actualizar modelos

        # fuego
        for fire in self.fires:
            if pygame.time.get_ticks() - fire.startTime >= fire.duration:
                fire.validity = False
            # jugador/es quemado/s
            for player in self.players:
                if fire.burn(player):
                    player.lives -= 1
                    player.repeatLevel(self.city)
                # quitar vida, restart game, nose

            # pacos quemados
            for policeman in self.policemen:
                if fire.burn(policeman):
                    policeman.alive = False
                    self.score += 200

            # muros quemados
            for wall in self.softWalls:
                if fire.burn(wall):
                    wall.validity = False
                    self.score += 100

            # powerUps quemados (se eliminó esta parte del código porque los powerUps son inmortales)
            """
            for powerUp in self.powerUps:
                if fire.burn(powerUp) and powerUp.type != 'door' and self.city[powerUp.i, powerUp.j, 2] == 0:
                    powerUp.validity = False
            """

        # jugador/es
        for player in self.players:
            player.alive = player.lives > 0
            if player.inmortal and (pygame.time.get_ticks() - player.inmortalStart) / 1000.0 >= player.inmortalTime:
                player.setMortal()

        # enemigos
        for policeman in self.policemen:
            policeman.autoMove(self.city)
            for player in self.players:
                if policeman.touch(player):
                    player.lives -= 1
                    player.repeatLevel(self.city)

        # bombas
        for bomb in self.bombs:
            if pygame.time.get_ticks() - bomb.startTime >= bomb.explosionTime:
                bomb.explode(self.city, self.fires)
                bomb.validity = False

            # actualizar

        # muros

        # powerUp
        for powerUp in self.powerUps:
            for player in self.players:
                if powerUp.touch(player):
                    powerUp.used(player)
            # 3 casos: jugador gana solo, jugador gana solo en multiplayer, dos jugadores ganan}
            if powerUp.type == 'door' and len(self.policemen) == 0:
                if self.multiplayer:
                    if self.player.lives <= 0 and powerUp.touch(self.player2):
                        print("Felicidades Jugador 2, ganaste!")
                        print("Puntuación:", self.score)
                        pygame.quit()
                        sys.exit()
                    elif self.player2.lives <= 0 and powerUp.touch(self.player):
                        print("Felicidades Jugador 1, ganaste!")
                        print("Puntuación:", self.score)
                        pygame.quit()
                        sys.exit()
                    elif powerUp.touch(self.player) and powerUp.touch(self.player2):
                        print("Felicidades, ganaste!")
                        print("Puntuación:", self.score)
                        pygame.quit()
                        sys.exit()

                elif powerUp.touch(self.player):
                    print("Felicidades, ganaste!")
                    print("Puntuación:", self.score)
                    pygame.quit()
                    sys.exit()

        # remover objetos no válidos

        # fuego
        for i in range(len(self.fires) - 1, -1, -1):
            if not self.fires[i].validity:
                self.fires.pop(i)
        # bombas
        for i in range(len(self.bombs) - 1, -1, -1):
            if not self.bombs[i].validity:
                m = int(self.bombs[i].y / square_length)
                n = int(self.bombs[i].x / square_length)
                self.city[m, n, 2] = 0
                self.bombs.pop(i)

        # enemigos
        for i in range(len(self.policemen) - 1, -1, -1):
            if not self.policemen[i].alive:
                self.policemen.pop(i)

        # muros suaves
        for i in range(len(self.softWalls) - 1, -1, -1):
            if not self.softWalls[i].validity:
                m = int(self.softWalls[i].y / square_length)
                n = int(self.softWalls[i].x / square_length)
                self.city[m, n, 2] = 0
                self.softWalls.pop(i)

        # powerups
        for i in range(len(self.powerUps) - 1, -1, -1):
            if not self.powerUps[i].validity:
                m = int(self.softWalls[i].y / square_length)
                n = int(self.softWalls[i].x / square_length)
                self.city[m, n, 3] = 0
                self.powerUps.pop(i)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    if not self.pausa:
                        self.pause()
                        self.pausa = True
                    else:
                        self.unpause()
                        self.pausa = False

                if self.multiplayer:  # configuración de teclas de multijugador
                    if event.key == pygame.K_l:
                        self.player.placeBomb(self.city, self.bombs)
                    if event.key == pygame.K_c:
                        self.player2.placeBomb(self.city, self.bombs)
                else:  # configuración de teclas estandar
                    if event.key == pygame.K_a:
                        self.player.placeBomb(self.city, self.bombs)

        # Teclas
        keys = pygame.key.get_pressed()

        # cuadrado en el que está centro del jugador:
        i = int(self.player.y / square_length)
        j = int(self.player.x / square_length)

        x_center = self.city[i, j, 1]
        y_center = self.city[i, j, 0]

        # Teclas de movimiento

        # jugador 1:
        if keys[pygame.K_UP]:
            next_square = self.city[i - 1, j, 2]  # cuadrado al que se está avanzando
            crash_distance = abs(
                self.city[i - 1, j, 0] - self.player.y) - square_length  # distancia del jugador al muro
            direction = '-y'

            if next_square == 0:  # próximo cuadrado está vacío
                # 2 casos especiales: esquinas ocupadas y jugador no centrado
                corner1 = self.city[i - 1, j + 1, 2]
                uncentered_player1 = x_center < self.player.x <= x_center + square_length / 2
                distance_to_center = abs(x_center - self.player.x)
                corner2 = self.city[i - 1, j - 1, 2]
                uncentered_player2 = x_center - square_length / 2 <= self.player.x < x_center

                if corner1 != 0 and uncentered_player1:
                    if distance_to_center < self.player.speed / sqrt(2):
                        self.player.move(direction, distance_to_center)
                        self.player.move('-x', distance_to_center)
                    else:
                        self.player.move(direction, self.player.speed / sqrt(2))
                        self.player.move('-x', self.player.speed / sqrt(2))
                elif corner2 != 0 and uncentered_player2:
                    if distance_to_center < self.player.speed / sqrt(2):
                        self.player.move(direction, distance_to_center)
                        self.player.move('x', distance_to_center)
                    else:
                        self.player.move(direction, self.player.speed / sqrt(2))
                        self.player.move('x', self.player.speed / sqrt(2))
                else:
                    self.player.move(direction)

            elif crash_distance > 0:  # próximo cuadrado está ocupado, pero aún se puede avanzar
                if crash_distance <= self.player.speed:
                    self.player.move(direction, crash_distance)
                else:
                    self.player.move(direction)
        if keys[pygame.K_DOWN]:
            next_square = self.city[i + 1, j, 2]  # cuadrado al que se está avanzando
            crash_distance = abs(
                self.city[i + 1, j, 0] - self.player.y) - square_length  # distancia del jugador al muro
            direction = 'y'

            if next_square == 0:  # próximo cuadrado está vacío
                # 2 casos especiales: esquinas ocupadas y jugador no centrado
                corner1 = self.city[i + 1, j + 1, 2]
                uncentered_player1 = x_center < self.player.x <= x_center + square_length / 2
                distance_to_center = abs(x_center - self.player.x)
                corner2 = self.city[i + 1, j - 1, 2]
                uncentered_player2 = x_center - square_length / 2 <= self.player.x < x_center

                if corner1 != 0 and uncentered_player1:
                    if distance_to_center < self.player.speed / sqrt(2):
                        self.player.move(direction, distance_to_center)
                        self.player.move('-x', distance_to_center)
                    else:
                        self.player.move(direction, self.player.speed / sqrt(2))
                        self.player.move('-x', self.player.speed / sqrt(2))
                elif corner2 != 0 and uncentered_player2:
                    if distance_to_center < self.player.speed / sqrt(2):
                        self.player.move(direction, distance_to_center)
                        self.player.move('x', distance_to_center)
                    else:
                        self.player.move(direction, self.player.speed / sqrt(2))
                        self.player.move('x', self.player.speed / sqrt(2))
                else:
                    self.player.move(direction)

            elif crash_distance > 0:  # próximo cuadrado está ocupado, pero aún se puede avanzar
                if crash_distance <= self.player.speed:
                    self.player.move(direction, crash_distance)
                else:
                    self.player.move(direction)
        if keys[pygame.K_RIGHT]:
            next_square = self.city[i, j + 1, 2]  # cuadrado al que se está avanzando
            crash_distance = abs(
                self.city[i, j + 1, 1] - self.player.x) - square_length  # distancia del jugador al muro
            direction = 'x'

            if next_square == 0:  # próximo cuadrado está vacío
                # 2 casos especiales: esquinas ocupadas y jugador no centrado
                corner1 = self.city[i + 1, j + 1, 2]
                corner2 = self.city[i - 1, j + 1, 2]

                uncentered_player1 = y_center < self.player.y <= y_center + square_length / 2
                uncentered_player2 = y_center - square_length / 2 <= self.player.y < y_center

                distance_to_center = abs(y_center - self.player.y)

                if corner1 != 0 and uncentered_player1:
                    if distance_to_center < self.player.speed / sqrt(2):
                        self.player.move(direction, distance_to_center)
                        self.player.move('-y', distance_to_center)
                    else:
                        self.player.move(direction, self.player.speed / sqrt(2))
                        self.player.move('-y', self.player.speed / sqrt(2))
                elif corner2 != 0 and uncentered_player2:
                    if distance_to_center < self.player.speed / sqrt(2):
                        self.player.move(direction, distance_to_center)
                        self.player.move('y', distance_to_center)
                    else:
                        self.player.move(direction, self.player.speed / sqrt(2))
                        self.player.move('y', self.player.speed / sqrt(2))
                else:
                    self.player.move(direction)

            elif crash_distance > 0:  # próximo cuadrado está ocupado, pero aún se puede avanzar
                if crash_distance <= self.player.speed:
                    self.player.move(direction, crash_distance)
                else:
                    self.player.move(direction)
        if keys[pygame.K_LEFT]:
            next_square = self.city[i, j - 1, 2]  # cuadrado al que se está avanzando
            crash_distance = abs(
                self.city[i, j - 1, 1] - self.player.x) - square_length  # distancia del jugador al muro
            direction = '-x'

            if next_square == 0:  # próximo cuadrado está vacío
                # 2 casos especiales: esquinas ocupadas y jugador no centrado
                corner1 = self.city[i + 1, j - 1, 2]
                corner2 = self.city[i - 1, j - 1, 2]

                uncentered_player1 = y_center < self.player.y <= y_center + square_length / 2
                uncentered_player2 = y_center - square_length / 2 <= self.player.y < y_center

                distance_to_center = abs(y_center - self.player.y)

                if corner1 != 0 and uncentered_player1:
                    if distance_to_center < self.player.speed / sqrt(2):
                        self.player.move(direction, distance_to_center)
                        self.player.move('-y', distance_to_center)
                    else:
                        self.player.move(direction, self.player.speed / sqrt(2))
                        self.player.move('-y', self.player.speed / sqrt(2))
                elif corner2 != 0 and uncentered_player2:
                    if distance_to_center < self.player.speed / sqrt(2):
                        self.player.move(direction, distance_to_center)
                        self.player.move('y', distance_to_center)
                    else:
                        self.player.move(direction, self.player.speed / sqrt(2))
                        self.player.move('y', self.player.speed / sqrt(2))
                else:
                    self.player.move(direction)

            elif crash_distance > 0:  # próximo cuadrado está ocupado, pero aún se puede avanzar
                if crash_distance <= self.player.speed:
                    self.player.move(direction, crash_distance)
                else:
                    self.player.move(direction)

        # jugador 2:
        if self.multiplayer:

            i = int(self.player2.y / square_length)
            j = int(self.player2.x / square_length)

            x_center = self.city[i, j, 1]
            y_center = self.city[i, j, 0]

            if keys[pygame.K_w]:
                next_square = self.city[i - 1, j, 2]  # cuadrado al que se está avanzando
                crash_distance = abs(
                    self.city[i - 1, j, 0] - self.player2.y) - square_length  # distancia del jugador al muro
                direction = '-y'

                if next_square == 0:  # próximo cuadrado está vacío
                    # 2 casos especiales: esquinas ocupadas y jugador no centrado
                    corner1 = self.city[i - 1, j + 1, 2]
                    uncentered_player1 = x_center < self.player2.x <= x_center + square_length / 2
                    distance_to_center = abs(x_center - self.player2.x)
                    corner2 = self.city[i - 1, j - 1, 2]
                    uncentered_player2 = x_center - square_length / 2 <= self.player2.x < x_center

                    if corner1 != 0 and uncentered_player1:
                        if distance_to_center < self.player2.speed / sqrt(2):
                            self.player2.move(direction, distance_to_center)
                            self.player2.move('-x', distance_to_center)
                        else:
                            self.player2.move(direction, self.player2.speed / sqrt(2))
                            self.player2.move('-x', self.player2.speed / sqrt(2))
                    elif corner2 != 0 and uncentered_player2:
                        if distance_to_center < self.player2.speed / sqrt(2):
                            self.player2.move(direction, distance_to_center)
                            self.player2.move('x', distance_to_center)
                        else:
                            self.player2.move(direction, self.player2.speed / sqrt(2))
                            self.player2.move('x', self.player2.speed / sqrt(2))
                    else:
                        self.player2.move(direction)

                elif crash_distance > 0:  # próximo cuadrado está ocupado, pero aún se puede avanzar
                    if crash_distance <= self.player2.speed:
                        self.player2.move(direction, crash_distance)
                    else:
                        self.player2.move(direction)
            if keys[pygame.K_s]:
                next_square = self.city[i + 1, j, 2]  # cuadrado al que se está avanzando
                crash_distance = abs(
                    self.city[i + 1, j, 0] - self.player2.y) - square_length  # distancia del jugador al muro
                direction = 'y'

                if next_square == 0:  # próximo cuadrado está vacío
                    # 2 casos especiales: esquinas ocupadas y jugador no centrado
                    corner1 = self.city[i + 1, j + 1, 2]
                    uncentered_player1 = x_center < self.player2.x <= x_center + square_length / 2
                    distance_to_center = abs(x_center - self.player2.x)
                    corner2 = self.city[i + 1, j - 1, 2]
                    uncentered_player2 = x_center - square_length / 2 <= self.player2.x < x_center

                    if corner1 != 0 and uncentered_player1:
                        if distance_to_center < self.player2.speed / sqrt(2):
                            self.player2.move(direction, distance_to_center)
                            self.player2.move('-x', distance_to_center)
                        else:
                            self.player2.move(direction, self.player2.speed / sqrt(2))
                            self.player2.move('-x', self.player2.speed / sqrt(2))
                    elif corner2 != 0 and uncentered_player2:
                        if distance_to_center < self.player2.speed / sqrt(2):
                            self.player2.move(direction, distance_to_center)
                            self.player2.move('x', distance_to_center)
                        else:
                            self.player2.move(direction, self.player2.speed / sqrt(2))
                            self.player2.move('x', self.player2.speed / sqrt(2))
                    else:
                        self.player2.move(direction)

                elif crash_distance > 0:  # próximo cuadrado está ocupado, pero aún se puede avanzar
                    if crash_distance <= self.player2.speed:
                        self.player2.move(direction, crash_distance)
                    else:
                        self.player2.move(direction)
            if keys[pygame.K_d]:
                next_square = self.city[i, j + 1, 2]  # cuadrado al que se está avanzando
                crash_distance = abs(
                    self.city[i, j + 1, 1] - self.player2.x) - square_length  # distancia del jugador al muro
                direction = 'x'

                if next_square == 0:  # próximo cuadrado está vacío
                    # 2 casos especiales: esquinas ocupadas y jugador no centrado
                    corner1 = self.city[i + 1, j + 1, 2]
                    corner2 = self.city[i - 1, j + 1, 2]

                    uncentered_player1 = y_center < self.player2.y <= y_center + square_length / 2
                    uncentered_player2 = y_center - square_length / 2 <= self.player2.y < y_center

                    distance_to_center = abs(y_center - self.player2.y)

                    if corner1 != 0 and uncentered_player1:
                        if distance_to_center < self.player2.speed / sqrt(2):
                            self.player2.move(direction, distance_to_center)
                            self.player2.move('-y', distance_to_center)
                        else:
                            self.player2.move(direction, self.player2.speed / sqrt(2))
                            self.player2.move('-y', self.player2.speed / sqrt(2))
                    elif corner2 != 0 and uncentered_player2:
                        if distance_to_center < self.player2.speed / sqrt(2):
                            self.player2.move(direction, distance_to_center)
                            self.player2.move('y', distance_to_center)
                        else:
                            self.player2.move(direction, self.player2.speed / sqrt(2))
                            self.player2.move('y', self.player2.speed / sqrt(2))
                    else:
                        self.player2.move(direction)

                elif crash_distance > 0:  # próximo cuadrado está ocupado, pero aún se puede avanzar
                    if crash_distance <= self.player2.speed:
                        self.player2.move(direction, crash_distance)
                    else:
                        self.player2.move(direction)
            if keys[pygame.K_a]:
                next_square = self.city[i, j - 1, 2]  # cuadrado al que se está avanzando
                crash_distance = abs(
                    self.city[i, j - 1, 1] - self.player2.x) - square_length  # distancia del jugador al muro
                direction = '-x'

                if next_square == 0:  # próximo cuadrado está vacío
                    # 2 casos especiales: esquinas ocupadas y jugador no centrado
                    corner1 = self.city[i + 1, j - 1, 2]
                    corner2 = self.city[i - 1, j - 1, 2]

                    uncentered_player1 = y_center < self.player2.y <= y_center + square_length / 2
                    uncentered_player2 = y_center - square_length / 2 <= self.player2.y < y_center

                    distance_to_center = abs(y_center - self.player2.y)

                    if corner1 != 0 and uncentered_player1:
                        if distance_to_center < self.player2.speed / sqrt(2):
                            self.player2.move(direction, distance_to_center)
                            self.player2.move('-y', distance_to_center)
                        else:
                            self.player2.move(direction, self.player2.speed / sqrt(2))
                            self.player2.move('-y', self.player2.speed / sqrt(2))
                    elif corner2 != 0 and uncentered_player2:
                        if distance_to_center < self.player2.speed / sqrt(2):
                            self.player2.move(direction, distance_to_center)
                            self.player2.move('y', distance_to_center)
                        else:
                            self.player2.move(direction, self.player2.speed / sqrt(2))
                            self.player2.move('y', self.player2.speed / sqrt(2))
                    else:
                        self.player2.move(direction)

                elif crash_distance > 0:  # próximo cuadrado está ocupado, pero aún se puede avanzar
                    if crash_distance <= self.player2.speed:
                        self.player2.move(direction, crash_distance)
                    else:
                        self.player2.move(direction)


        if self.multiplayer and self.player.lives <= 0 and self.player2.lives <= 0:
            print("Game Over! Perdieron :(")
            pygame.quit()
            sys.exit()
        elif not self.multiplayer and self.player.lives <= 0:
            print("Game Over! Perdiste :(")
            pygame.quit()
            sys.exit()
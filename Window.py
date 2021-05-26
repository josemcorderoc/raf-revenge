import pygame
from OpenGL.raw.GL.VERSION.GL_1_0 import glClearColor, glClear, GL_COLOR_BUFFER_BIT

from constants import *

class Window:

    def __init__(self, screen, players, softWalls, hardWalls, powerUps, policemen,
                 bombs, fires, fonts, leftTime, score, multiplayer):
        self.players = players
        self.screen = screen

        self.color = (190, 190, 190)

        self.softWalls = softWalls
        self.hardWalls = hardWalls
        self.bombs = bombs
        self.fires = fires
        self.powerUps = powerUps

        self.policemen = policemen
        self.fonts = fonts
        self.leftTime = leftTime
        self.score = score
        self.multiplayer = multiplayer

    def clean(self):
        if OPENGLMODE:
            glClearColor(self.color[0]/255.0, self.color[1]/255.0, self.color[2]/255.0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
        else:
            self.screen.fill(self.color)

    def draw(self):
        for powerUp in self.powerUps:
            powerUp.draw(self.screen)

        for softWall in self.softWalls:
            softWall.draw(self.screen)

        for hardWall in self.hardWalls:
            hardWall.draw(self.screen)

        for bomb in self.bombs:
            bomb.draw(self.screen)

        for fire in self.fires:
            fire.draw(self.screen)

        for policeman in self.policemen:
            policeman.draw(self.screen)

        for player in self.players:
            player.draw(self.screen)

        if OPENGLMODE:
            pass
        else:
            self.screen.scroll(0, 100)

            pygame.draw.rect(self.screen, (0,0,0), [0, 0, WIDTH, 100])

            text1 = self.fonts[0].render("VIDAS:", 1, (255, 255, 255))
            vidas = self.fonts[1].render(str(self.players[0].lives), 1, (255, 255, 255))

            text2 = self.fonts[0].render("PUNTUACION:", 1, (255, 255, 255))
            puntuacion = self.fonts[1].render(format(self.score, '05'), 1, (255, 255, 255))

            text3 = self.fonts[0].render("TIEMPO:", 1, (255, 255, 255))
            time = self.fonts[1].render(format(self.leftTime/1000, '03'), 1, (255, 255, 255))

            text4 = self.fonts[0].render("BOMBAS:", 1, (255, 255, 255))
            bombs = self.fonts[1].render(format(self.players[0].maxBombs - self.players[0].placedBombs, '02') , 1, (255, 255, 255))

            if self.multiplayer:
                vidas1 = self.fonts[2].render(str(self.players[0].lives) + " (P1)", 1, (255, 255, 255))
                vidas2 = self.fonts[2].render(str(self.players[1].lives) + " (P2)", 1, (255, 255, 255))
                bombs1 = self.fonts[2].render(format(self.players[0].maxBombs - self.players[0].placedBombs,
                                                     '02') + " (P1)", 1, (255, 255, 255))
                bombs2 = self.fonts[2].render(format(self.players[1].maxBombs - self.players[1].placedBombs,
                                                     '02') + " (P2)", 1, (255, 255, 255))

            rafmini = pygame.image.load("Resources/rafmini.png")

            self.screen.blit(text1, (490, 10))
            self.screen.blit(text2, (280, 10))
            self.screen.blit(text3, (130, 10))
            self.screen.blit(text4, (620, 10))

            self.screen.blit(puntuacion, (305, 45))
            self.screen.blit(time, (150, 45))

            self.screen.blit(rafmini, (10, 0))

            if self.multiplayer:
                self.screen.blit(vidas1, (505, 45))
                self.screen.blit(vidas2, (505, 70))
                self.screen.blit(bombs1, (640, 45))
                self.screen.blit(bombs2, (640, 70))
            else:
                self.screen.blit(vidas, (515, 45))
                self.screen.blit(bombs, (650, 45))

        pygame.display.flip()
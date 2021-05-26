import pygame

from Controller import Controller

program = Controller()
clock = pygame.time.Clock()

program.setScene()

while True:
    clock.tick(60)
    program.update()

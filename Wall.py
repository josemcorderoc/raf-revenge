from OpenGL.raw.GL.VERSION.GL_1_0 import glColor3f, glBegin, glVertex2f, GL_LINES, glEnd, GL_QUADS

from constants import *


class Wall:
    def __init__(self, x_pos, y_pos, type, image=None):
        self.x = x_pos
        self.y = y_pos
        self.type = type

        if type == 'hard':
            self.color = (105 / 255.0, 105 / 255.0, 105 / 255.0)
            self.linecolor = (1.0, 1.0, 1.0)
        elif type == 'soft':
            self.color = (238 / 255.0, 60 / 255.0, 73 / 255.0)
            self.linecolor = (1.0, 1.0, 1.0)

        self.validity = True
        self.sprite = image

    def draw(self, surface):
        if self.sprite == None:
            # square = [self.x - square_length/2, self.y - square_length/2, square_length, square_length]
            # pygame.draw.rect(surface, self.color, square)

            glColor3f(*self.color)
            # glRectf(self.x - square_length / 2, self.y - square_length / 2, self.x - square_length / 2, self.y + square_length / 2)
            glBegin(GL_QUADS)
            glVertex2f(self.x - square_length / 2, self.y - square_length / 2)
            glVertex2f(self.x + square_length / 2, self.y - square_length / 2)
            glVertex2f(self.x + square_length / 2, self.y + square_length / 2)
            glVertex2f(self.x - square_length / 2, self.y + square_length / 2)
            glEnd()

            glColor3f(*self.linecolor)
            glBegin(GL_LINES)  # líneas de ladrillo
            glVertex2f(self.x - square_length / 2, self.y - square_length / 2)
            glVertex2f(self.x + square_length / 2, self.y - square_length / 2)

            glVertex2f(self.x - square_length / 2, self.y - square_length / 4)
            glVertex2f(self.x + square_length / 2, self.y - square_length / 4)

            glVertex2f(self.x - square_length / 2, self.y)
            glVertex2f(self.x + square_length / 2, self.y)

            glVertex2f(self.x - square_length / 2, self.y + square_length / 4)
            glVertex2f(self.x + square_length / 2, self.y + square_length / 4)

            glVertex2f(self.x - square_length / 2, self.y + square_length / 2)
            glVertex2f(self.x + square_length / 2, self.y + square_length / 2)

            glVertex2f(self.x, self.y - square_length / 2)
            glVertex2f(self.x, self.y - square_length / 4)

            glVertex2f(self.x, self.y)
            glVertex2f(self.x, self.y + square_length / 4)

            glVertex2f(self.x - square_length / 2, self.y - square_length / 2)
            glVertex2f(self.x - square_length / 2, self.y - square_length / 4)

            glVertex2f(self.x - square_length / 2, self.y)
            glVertex2f(self.x - square_length / 2, self.y + square_length / 4)

            glVertex2f(self.x + square_length / 2, self.y - square_length / 2)
            glVertex2f(self.x + square_length / 2, self.y - square_length / 4)

            glVertex2f(self.x + square_length / 2, self.y)
            glVertex2f(self.x + square_length / 2, self.y + square_length / 4)

            glVertex2f(self.x - square_length / 4, self.y - square_length / 4)
            glVertex2f(self.x - square_length / 4, self.y)

            glVertex2f(self.x - square_length / 4, self.y + square_length / 4)
            glVertex2f(self.x - square_length / 4, self.y + square_length / 2)

            glVertex2f(self.x + square_length / 4, self.y - square_length / 4)
            glVertex2f(self.x + square_length / 4, self.y)

            glVertex2f(self.x + square_length / 4, self.y + square_length / 4)
            glVertex2f(self.x + square_length / 4, self.y + square_length / 2)
            glEnd()
        else:
            surface.blit(self.sprite, (int(self.x) - square_length / 2, int(self.y) - square_length / 2))

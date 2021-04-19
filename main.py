# coding:utf-8

import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    rows = 20
    width = 500

    def __init__(self, start, dir_x=0, dir_y=0, color=(91, 188, 82)):
        self.pos = start
        self.dir_x = 0
        self.dir_y = 0
        self.color = color

    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)

    # Boolean "eyes" means that is the first cube
    # I put it as "True" to know which cube of the snake will have eyes
    def draw(self, surface, eyes=False):
        dis = self.width // self.rows  # Width/Height of each cube
        r = self.pos[0]  # Current row
        c = self.pos[1]  # Current column
        # Rectangle of the snake (inside the box, in order to see the white line)
        pygame.draw.rect(surface, self.color, (r * dis + 1, c * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circle_middle = (r * dis + centre - radius, c * dis + 8)
            circle_middle_2 = (r * dis + dis - radius * 2, c * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        # Snake directions
        self.dir_x = 0
        self.dir_y = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:  # or keys[pygame.K_q]:
                    self.dir_x = -1
                    self.dir_y = 0
                    # Remember the position where the player turned
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_RIGHT]:  # or keys[pygame.K_d]:
                    self.dir_x = 1
                    self.dir_y = 0
                    # Remember the position where the player turned
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_UP]:  # or keys[pygame.K_z]:
                    self.dir_x = 0
                    self.dir_y = -1
                    # Remember the position where the player turned
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]
                elif keys[pygame.K_DOWN]:  # or keys[pygame.K_s]:
                    self.dir_x = 0
                    self.dir_y = 1
                    # Remember the position where the player turned
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

        # i = index, c = cube's object, p = c's position, turn = position where the cube turns
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                # When the snake goes beyond the edges of the window
                if c.dir_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dir_x == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dir_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                elif c.dir_y == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                else:
                    c.move(c.dir_x, c.dir_y)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dir_x = 0
        self.dir_y = 0

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dir_x, tail.dir_y

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dir_x = dx
        self.body[-1].dir_y = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redraw_window(surface):
    global rows, width, s, snack
    surface.fill((142, 90, 0))
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)
    pass


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    window = pygame.display.set_mode((width, width))
    gameIcon = pygame.image.load('snakeIcon.png')
    pygame.display.set_icon(gameIcon)
    s = Snake(pos=(10, 10), color=(91, 188, 82))
    snack = Cube(random_snack(rows, s), color=(241, 11, 11))

    while True:
        pygame.time.delay(100)
        s.move()
        if s.body[0].pos == snack.pos:
            s.add_cube()
            snack = Cube(random_snack(rows, s), color=(241, 11, 11))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                # font = pygame.font.SysFont("comicsansms", 20)
                message_box('You lost !', 'Score: {} \nPlay again...'.format(len(s.body)))
                s.reset((10, 10))
                break

        redraw_window(window)

    pass


main()

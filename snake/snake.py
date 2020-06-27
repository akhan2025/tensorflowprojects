import random
import pygame
import tkinter as tk
from tkinter import messagebox
import neat
import os
from pynput.keyboard import Key, Controller

keyboard = Controller()

class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, directionx = 1, directiony = 0, color = (0, 255, 0)):
        self.pos = start
        self.directionx = 1
        self.directiony = 0
        self.color = color

    def move(self, directionx, directiony):
        self.directionx = directionx
        self.directiony = directiony
        self.pos = (self.pos[0] + self.directionx, self.pos[1] + directiony)

    def draw(self, surface, color = False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        if color == True:
            self.color = (255, 255, 0)
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.directionx = 0
        self.directiony = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.directionx = -1
                    self.directiony = 0
                    self.turns[self.head.pos[:]] = [self.directionx, self.directiony]

                elif keys[pygame.K_RIGHT]:
                    self.directionx = 1
                    self.directiony = 0
                    self.turns[self.head.pos[:]] = [self.directionx, self.directiony]

                elif keys[pygame.K_UP]:
                    self.directionx = 0
                    self.directiony = -1
                    self.turns[self.head.pos[:]] = [self.directionx, self.directiony]

                elif keys[pygame.K_DOWN]:
                    self.directionx = 0
                    self.directiony = 1
                    self.turns[self.head.pos[:]] = [self.directionx, self.directiony]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.directionx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.directionx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.directiony == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.directiony == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.directionx, c.directiony)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.directionx = 0
        self.directiony = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.directionx, tail.directiony

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].directionx = dx
        self.body[-1].directiony = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.directionx = 0
        self.directiony = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.directionx, tail.directiony

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].directionx = dx
        self.body[-1].directiony = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(rows, w, surface):
    space = w // rows

    x = 0
    y = 0

    for z in range(rows):
        x = x + space
        y = y + space

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, snakes, snack
    surface.fill((0, 0, 0))
    for snake in snakes:
        snake.draw(surface)
    snack.draw(surface)
    drawGrid(rows, width, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main(genomes, config):
    global width, rows, snakes, snack
    nets =[]
    ge = []
    snakes = []
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        snakes.append(Snake((0, 255, 0), (10, 10)))
        g.fitness = 0
        ge.append(g)

    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))

    for snake in snakes:
        snack = Cube(randomSnack(rows, snake), color = (255, 0, 0))

    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        for q, snake in enumerate(snakes):
            snake.move()
            ge[q].fitness += 0.1

            snack_loc = list(snack.pos)
            output = nets[q].activate(snake.directionx, snake.directiony, snack_loc[0], snack_loc[1])
            index = 0
            for i, x in enumerate(output):
                if x > output[index]:
                    index = i

            if index > 0:
                keyboard.press('w')
            elif index > 1:
                keyboard.press('a')
            elif index > 2:
                keyboard.press('s')
            elif index > 3:
                keyboard.press('d')

            if snake.body[0].pos == snack.pos:
                snake.addCube()
                snack = Cube(randomSnack(rows, snake), color = (255, 0, 0))
                ge[q].fitness += 10
    
            for x in range(len(snake.body)):
                if snake.body[x].pos in list(map(lambda z: z.pos, snake.body[x + 1:])):
                    ge[q].fitness -= 1
                    snakes.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            if len(snakes) == 0:
                flag = False
                break

        redrawWindow(win)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
import pygame
from pygame.locals import *
import random
from collections import Counter


class Cell:
    pass


class GameOfLife:
    def __init__(self, width = 640, height = 480, cell_size = 10, speed = 100):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)
        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Скорость протекания игры
        self.speed = speed
        self.clist = []
        self.pre_clist = []
    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))


    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            self.update_cell_list()
            for frame in range(10):
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            print(pos)
                            pos_cell=[0,0]
                            pos_cell[0],pos_cell[1] = pos[0] // self.cell_size, pos[1] // self.cell_size
                            print(pos_cell)
                            self.clist[pos_cell[1]][pos_cell[0]] = 2
                self.draw_cell_list(self.clist)
                self.draw_grid()
                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()


    def cell_list(self, randomize=False):
        for i in range(self.cell_height):
            self.clist.append([])
            for j in range(self.cell_width):
                if randomize:
                    state = 1 if random.randint(0,7)==1 else 0
                    self.clist[i].append(state)
        return self.clist


    def get_neighbours(self, cell):
        neighbours = []
        for y in range(-1,2):
            for x in range(-1,2):
                if x or y:
                    if cell.y+y>=0 and cell.x+x>=0 and cell.y+y<=self.cell_height-1 and cell.x+x<=self.cell_width-1:
                        cell_state = 1 if self.clist[cell.y+y][cell.x+x]!=0 else 0
                        neighbours.append(cell_state)
                    else:
                        neighbours.append(0)
        return Counter(neighbours)[1]


    def update_cell_list(self):
        self.pre_clist = self.clist
        for i,_ in enumerate(self.clist):
            for j,__ in enumerate(_):
                cell = Cell()
                cell.y = i
                cell.x = j 
                neighbours = self.get_neighbours(cell)
                if self.clist[cell.y][cell.x]>0:
                    if neighbours==2 or neighbours==3 :
                        self.pre_clist[cell.y][cell.x] = 1
                    else: 
                        self.pre_clist[cell.y][cell.x] = 0
                else:
                    if neighbours==3:
                        self.pre_clist[cell.y][cell.x] = 2
        self.clist = self.pre_clist


    def draw_cell_list(self, rects):
        for i,_ in enumerate(rects):
            for j,el in enumerate(_):
                if el == 1:
                    color = "orange"
                elif el == 2:
                    color = "red"
                else:
                    color = "white"
                y = i*self.cell_size
                x = j*self.cell_size
                pygame.draw.rect(self.screen,
                                 pygame.Color(color),
                                 (x, y, self.cell_size, self.cell_size)
                                   )


if __name__ == '__main__':
    from pprint import pprint as pp
    game = GameOfLife()
    clist = game.cell_list(randomize=True)
    game.draw_cell_list(clist)
    game.run()

from random import randint, random

import numpy as np

global EMPTY, NORTH, EAST, SOUTH, WEST, STAY, BORDER

EMPTY = 0
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
STAY = 5
BORDER = 6

class Fish():


    def __init__(self, shape:int, n_fishes:int=10):
        self._shape = shape+2
        self._n_fishes = n_fishes
        self._grid = []


    def generate(self):
        self._grid = BORDER*np.ones((self._shape, self._shape))
        for i in range(1, self._shape-1):
            for j in range(1, self._shape-1):
                self._grid[i][j] = 0
        self._summon()
        return self._grid


    def _summon(self):
        for i in range(1, self._shape-1):
            for j in range(1, self._shape-1):
                if random() <= self._n_fishes/((self._shape-2)**2):
                    self._grid[i][j] = randint(1, 4)
                else:
                    self._grid[i][j] = EMPTY


    def swim(self, time:int=1):
        n = len(self._grid) - 2
        for i in range(1, n+1):
            for j in range(1, n+1):
                Nfish = self._grid[i-1][j]
                Efish = self._grid[i][j+1]
                Sfish = self._grid[i+1][j]
                Wfish = self._grid[i][j-1]
                site = self._grid[i][j]
                crowd_level = [Nfish, Efish, Sfish, Wfish]
                directions = [NORTH, EAST, SOUTH, WEST]
                
                if self._grid[i][j] == NORTH:
                    if self._grid[i-1][j] == EMPTY:
                        self._grid[i][j] = EMPTY
                        self._grid[i-1][j] = np.random.choice([EAST, SOUTH, WEST])
                    else:
                        minimal_crowd = min(crowd_level)
                        preferable = []
                        if minimal_crowd == 1:
                            for index in range(4):
                                if crowd_level[index] == 1:
                                    preferable.append(directions[index])
                            self._grid[i][j] = np.random.choice(preferable)
                        else:
                            self._grid[i][j] = np.random.choice(directions, size=int(len(directions) > 0))
                
                if self._grid[i][j] == EAST:
                    if self._grid[i][j+1] == EMPTY:
                        self._grid[i][j] = EMPTY
                        self._grid[i][j+1] = np.random.choice([NORTH, SOUTH, WEST])
                    else:
                        minimal_crowd = min(crowd_level)
                        preferable = []
                        if minimal_crowd == 1:
                            for index in range(4):
                                if crowd_level[index] == 1:
                                    preferable.append(directions[index])
                            self._grid[i][j] = np.random.choice(preferable)
                        else:
                            self._grid[i][j] = np.random.choice(directions, size=int(len(directions) > 0))

                if self._grid[i][j] == SOUTH:
                    if self._grid[i+1][j] == EMPTY:
                        self._grid[i][j] = EMPTY
                        self._grid[i+1][j] = np.random.choice([EAST, NORTH, WEST])
                    else:
                        minimal_crowd = min(crowd_level)
                        preferable = []
                        if minimal_crowd == 1:
                            for index in range(4):
                                if crowd_level[index] == 1:
                                    preferable.append(directions[index])
                            self._grid[i][j] = np.random.choice(preferable)
                        else:
                            self._grid[i][j] = np.random.choice(directions, size=int(len(directions) > 0))

                if self._grid[i][j] == WEST:
                    if self._grid[i][j-1] == EMPTY:
                        self._grid[i][j] = EMPTY
                        self._grid[i][j-1] = np.random.choice([EAST, SOUTH, NORTH])
                    else:
                        minimal_crowd = min(crowd_level)
                        preferable = []
                        if minimal_crowd == 1:
                            for index in range(4):
                                if crowd_level[index] == 1:
                                    preferable.append(directions[index])
                            self._grid[i][j] = np.random.choice(preferable)
                        else:
                            self._grid[i][j] = np.random.choice(directions, size=int(len(directions) > 0))
        return self._grid


    def sense(self, food_grid):
        n = self._shape - 2
        for i in range(1, n+1):
            for j in range(1, n+1):
                if self._grid[i][j] != EMPTY:
                    site = self._grid[i][j]
                    Nfood = food_grid[i-1][j]
                    Efood = food_grid[i][j+1]
                    Sfood = food_grid[i+1][j]
                    Wfood = food_grid[i][j-1]
                    
                    sense_dir = [Nfood, Efood, Sfood, Wfood]
                    fish_dir = [NORTH, EAST, SOUTH, WEST]
                    max_sm = max(sense_dir)
                    direction = EMPTY
                    
                    if site == EMPTY:
                        self._grid[i][j] = direction
                        continue
                    if max_sm > 1:
                        for index in range(4):
                            if sense_dir[index] == max_sm:
                                direction = fish_dir[index]
                        self._grid[i][j] = direction
                else:
                    continue
        return self._grid


class Food():


    def __init__(self, shape:int):
        self._shape = shape + 2
        self._grid = np.zeros((self._shape, self._shape))
        n = self._shape - 2
        
        #specify pond area
        for i in range(1, n+1):
            for j in range(1, n+1):
                self._grid[i, j] = 1
  
    def dissolve(self):
        n = self._shape-2
        for i in range(1, n+1):
            for j in range(1, n+1):
                if self._grid[i, j] > 1 and self._grid[i, j] != 100:
                    smell_level = self._grid[i, j] - 2
                    self._grid[i, j] = max(smell_level, 1)
                if self._grid[i, j] == 100 and self._grid[i-1, j] == 1:
                    self._grid[i, j] = 1
        return self._grid


    def get_food_grid(self):
        return self._grid
    
    def reset(self):
        self._grid = np.zeros((self._shape, self._shape))
        n = self._shape - 2
        #specify pond area
        for i in range(1, n+1):
            for j in range(1, n+1):
                self._grid[i, j] = 1
        return self._grid

    def feed(self, x_pos, y_pos):
        RADIUS = int(self._shape - .5*self._shape)
        smell_level = 2
        if self._grid[y_pos, x_pos] != 0:
            for r in range(0, RADIUS):
                for i in range(y_pos - r, y_pos + r + 1):
                    for j in range(x_pos - r, x_pos + r + 1):
                        try:
                            if i >= 0 and j >= 0:
                                if self._grid[i, j] == 1 or smell_level < self._grid[i, j]:
                                    self._grid[i, j] = max(self._grid[i, j]+smell_level, 1)
                            else:
                                continue
                        except:
                            continue
        self._grid[y_pos, x_pos] = self._shape
        return self._grid
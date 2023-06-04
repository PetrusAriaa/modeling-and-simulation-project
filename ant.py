from random import random

import numpy as np


class Ant():
    _ant_prob = 0
    _shape = (0,0)
    _EDGE = 0
    
    #facing
    _NORTH = 1
    _EAST = 2
    _SOUTH = 3
    _WEST = 4
    
    def __init__(self, shape: tuple, edge: int) -> None:
        self.shape = shape
        self._ant_grid = np.zeros(shape)
        self._EDGE = edge
    
    def summon(self, ant_prob:float):
        self._ant_prob = ant_prob
        for i in range(self._EDGE, self.shape[0]-self._EDGE):
            for j in range(self._EDGE, self.shape[1]-self._EDGE):
                if random() <= ant_prob:
                    self._ant_grid[i][j] = 1
    
    def ant_map(self):
        return self._ant_grid
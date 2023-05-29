import numpy as np
import matplotlib.pyplot as plt
from random import random

class Forest():
    """Object untuk menjalankan simulasi burning forest
    menggunakan neighborhood Von Neumann.
    
    Args:    
        shape (__tuple__): area lahan
        edge (__int__): jarak batas akhir forest dengan ujung lahan
    
    Example:
    ---
    ```
    myForest = Forest(shape=(50,50), edge=3)
    myForest.createTree(tree_prob=.5)
    ```
    
    untuk menampilkan tree yang dibuat bisa menggunakan library `matplotlib`
    ::
    ```
    import matplotlib.pyplot as plt
    
    myForest = Forest(shape=(50,50), edge=3)
    myForest.createTree(tree_prob=.5)
    f = myForest.show_forest()
    
    figure = plt.imshow(f, cmap='Greens')
    ```
    """
    
    _tree_prob = 0
    _fire_prob = 0
    
    def __init__(self, shape:tuple, edge:int=3):
        self.forest_grid = np.zeros(shape)
        self.fire_grid = np.zeros(shape)
        self.tree_grid = np.zeros(shape)
        self.EDGE = edge
    
    
    def createTree(self, tree_prob) -> None:
        """Membuat tree secara random di dalam area Forest dengan
        probabilitas `tree_prob`

        Args:
            tree_prob (__float__): probabilitas adanya tree di koordinat (i,j).
            `0 < tree_prob < 1`
        """
        self._tree_prob = tree_prob
        for i in range(self.EDGE, self.forest_grid.shape[0]-self.EDGE):
            for j in range(self.EDGE, self.forest_grid.shape[1]-self.EDGE):
                if random() <= self._tree_prob:
                    self.tree_grid[i][j]=1
                    self.forest_grid[i][j]=1
     
    
    def show_forest(self):
        return self.forest_grid
    
    
    def initiate_fire(self, fire_prob):
        self.fire_prob = fire_prob
        for i in range(self.EDGE, self.forest_grid.shape[0]-self.EDGE):
            for j in range(self.EDGE, self.forest_grid.shape[1]-self.EDGE):
                if self.forest_grid[i][j] == 1:
                    if random() <= self.fire_prob:
                        self.fire_grid[i][j]=1
                        self.forest_grid[i][j]=.5
    
    
    def _fire(self, row, col):
        if self.forest_grid[row][col] == 1:
            if random() <= self.fire_prob:
                self.fire_grid[row][col]=1
                self.forest_grid[row][col]=.5

    
    def simulate(self):
        for i in range(self.EDGE, self.forest_grid.shape[0]-self.EDGE):
            for j in range(self.EDGE, self.forest_grid.shape[1]-self.EDGE):
                if self.forest_grid[i][j] == .5:
                    self._fire(i-1, j)
                    self._fire(i, j+1)
                    self._fire(i+1, j)
                    self._fire(i, j-1)
                    self.forest_grid[i][j]=0
                    self.tree_grid[i][j]=0
                    self.fire_grid[i][j]=0
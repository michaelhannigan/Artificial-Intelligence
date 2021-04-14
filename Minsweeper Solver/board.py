import random
import numpy as np
import time


class Board:
    def __init__(self, n):
        self.n_queen = n
        self.map = [[0 for j in range(n)] for i in range(n)]
        self.fit = 0
        self.encode_array = []
        self.start_time = time.time()

        for i in range(self.n_queen):
            j = random.randint(0, self.n_queen - 1)
            self.map[i][j] = 1

    def fitness(self):
        self.fit = 0
        for i in range(self.n_queen):
            for j in range(self.n_queen):
                if self.map[i][j] == 1:
                    for k in range(1, self.n_queen - i):
                        if self.map[i + k][j] == 1:
                            self.fit += 1
                        if j - k >= 0 and self.map[i + k][j - k] == 1:
                            self.fit += 1
                        if j + k < self.n_queen and self.map[i + k][j + k] == 1:
                            self.fit += 1

    def zero_map(self):
        for i in range(self.n_queen):
            for j in range(self.n_queen):
                self.map[i][j] = 0

    def get_non_attack(self):
        n = self.n_queen
        self.fitness()
        total_pair = n*(n-1)/2
        return total_pair - self.get_fit()

    def encode_map(self, arr):
        if len(arr) != len(self.map):
            print("The length of this list is not compatible with the given map size")
            return

        self.encode_array = arr
        self.zero_map()
        i = 0
        for j in arr:
            self.flip(i, j)
            i += 1

    def show(self):
        print(np.matrix(self.map))
        print("Fitness: ", self.fit)

    def flip(self, i, j):
        if self.map[i][j] == 0:
            self.map[i][j] = 1
        else:
            self.map[i][j] = 0

    def get_map(self):
        return self.map

    def get_fit(self):
        return self.fit

    def get_encode_array(self):
        self.encode_array = []
        for i in range(self.n_queen):
            for j in range(self.n_queen):
                if self.map[i][j] == 1:
                    self.encode_array.append(j)
        return self.encode_array

    def get_runtime(self):
        return '{:.0f}'.format(1000*(time.time()-self.start_time))

    def get_best(self, i, j):
        lowx = i
        lowy = j

        currMin = self.fit

        self.flip(i, j)

        for r in range(self.n_queen):
            if r != j:
                self.flip(i, r)
                self.fitness()
                weight = self.fit
                # self.show()

                if weight <= currMin:
                    currMin = weight

                    lowx = i
                    lowy = r
                    if weight == 0:
                        return [lowx, lowy, currMin]
                    self.flip(i, r)
                else:
                    self.flip(i, r)

        self.flip(lowx, lowy)
        return [lowx, lowy, currMin]

    def hill_climb_solver(self):
        numRestarts = 0
        currMin = 100000000
        while currMin > 0:
            numRestarts += 1
            for i in range(self.n_queen):
                for j in range(self.n_queen):
                    if self.map[i][j] == 1:
                        currY = j
                currMin = self.get_best(i, currY)[2]
                if currMin == 0:
                    print("Running time:", self.get_runtime(), "ms")
                    print("# of restart:", numRestarts)
                    self.show()
                    return


if __name__ == '__main__':
    test = Board(5)
    test.fitness()
    test.show()
import random
from board import Board
import time


class Genetic:
    def __init__(self, n):
        self.n = n
        self.A = Board(n)
        self.B = Board(n)
        self.C = Board(n)
        self.D = Board(n)
        self.E = Board(n)
        self.F = Board(n)
        self.G = Board(n)
        self.H = Board(n)

        self.curr_arr = [self.A, self.B, self.C, self.D, self.E, self.F, self.G, self.H]
        self.next_arr = []

        self.tuple = [[0, self.A], [0, self.B], [0, self.C], [0, self.D],
                      [0, self.E], [0, self.F], [0, self.G], [0, self.H]]

        self.start_time = time.time()
        self.restarts = 0

    def get_random(self):
        return random.randint(0, self.n - 1)

    # creates random lists to encode the objects
    def add_rand_encode(self):
        for i in range(len(self.curr_arr)):
            list_encode = []
            for j in range(self.n):
                list_encode.append(self.get_random())
            self.curr_arr[i] = Board(self.n)
            self.curr_arr[i].encode_map(list_encode)
            self.tuple[i][1] = self.curr_arr[i]
            # print(self.tuple[i][1])

    def calculate_fitness(self):
        total_non_attack = self.A.get_non_attack() + self.B.get_non_attack() + \
                           self.C.get_non_attack() + self.D.get_non_attack() + \
                           self.E.get_non_attack() + self.F.get_non_attack() + \
                           self.G.get_non_attack() + self.H.get_non_attack()
        for i in self.tuple:
            i[0] = (i[1].get_non_attack()) / total_non_attack

    def get_restarts(self):
        return self.restarts

    def choose_board(self):
        r = random.random()

        if r <= self.tuple[0][0]:
            return self.tuple[0][1]
        elif r <= self.tuple[1][0] + self.tuple[0][0]:
            return self.tuple[1][1]
        elif r <= self.tuple[2][0] + self.tuple[1][0] + self.tuple[0][0]:
            return self.tuple[2][1]
        elif r <= self.tuple[3][0] + self.tuple[2][0] + self.tuple[1][0] + self.tuple[0][0]:
            return self.tuple[3][1]
        elif r <= self.tuple[4][0] + self.tuple[3][0] + self.tuple[2][0] + self.tuple[1][0] + self.tuple[0][0]:
            return self.tuple[4][1]
        elif r <= self.tuple[5][0] + self.tuple[4][0] + self.tuple[3][0] + self.tuple[2][0] + self.tuple[1][0] + \
                self.tuple[0][0]:
            return self.tuple[5][1]
        elif r <= self.tuple[6][0] + self.tuple[5][0] + self.tuple[4][0] + self.tuple[3][0] + self.tuple[2][0] +\
                self.tuple[1][0] + self.tuple[0][0]:
            return self.tuple[6][1]
        else:
            return self.tuple[7][1]

    def cross_over(self, arr1, arr2):
        r = random.randint(1, self.n - 1)
        final = []

        upper_l = []
        upper_r = []
        lower_l = []
        lower_r = []

        for i in range(r):
            upper_l.append(arr1[i])
            lower_l.append(arr2[i])

        for i in range(r, self.n):
            upper_r.append(arr1[i])
            lower_r.append(arr2[i])

        rand_mutator_top = random.randint(-1, 4)
        rand_mutation_top = random.randint(0, 4)
        rand_mutator_bottom = random.randint(-1, 4)
        rand_mutation_bottom = random.randint(0, 4)

        top = upper_l + lower_r
        bottom = lower_l + upper_r

        if rand_mutator_top != -1:
            top[rand_mutator_top] = rand_mutation_top

        if rand_mutator_bottom != -1:
            bottom[rand_mutator_bottom] = rand_mutation_bottom

        final.append(top)
        final.append(bottom)

        return final

    def get_runtime(self):
        return '{:.0f}'.format(1000 * (time.time() - self.start_time))

    # maybe make this the solver??
    def genetic_solver(self):
        total_non_attack = self.n * (self.n - 1) / 2
        self.next_arr = []
        self.add_rand_encode()
        self.calculate_fitness()
        for i in range(4):
            new_board = self.choose_board()
            # print(new_board)
            self.next_arr.append(new_board)

        while True:
            self.restarts += 1
            self.calculate_fitness()
            self.next_arr = []

            for i in range(8):
                new_board = self.choose_board()
                self.next_arr.append(new_board)

            first = self.next_arr[0].get_encode_array()
            second = self.next_arr[1].get_encode_array()
            third = self.next_arr[2].get_encode_array()
            fourth = self.next_arr[3].get_encode_array()
            fifth = self.next_arr[4].get_encode_array()
            sixth = self.next_arr[5].get_encode_array()
            seventh = self.next_arr[6].get_encode_array()
            eigth = self.next_arr[7].get_encode_array()

            top1 = self.cross_over(first, second)
            bottom1 = self.cross_over(third, fourth)
            top2 = self.cross_over(fifth, sixth)
            bottom2 = self.cross_over(seventh, eigth)

            self.tuple[0][1].encode_map(top1[0])
            self.next_arr[0].encode_map(top1[0])

            self.tuple[1][1].encode_map(top1[1])
            self.next_arr[1].encode_map(top1[1])

            self.tuple[2][1].encode_map(bottom1[0])
            self.next_arr[2].encode_map(bottom1[0])

            self.tuple[3][1].encode_map(bottom1[1])
            self.next_arr[3].encode_map(bottom1[1])

            self.tuple[4][1].encode_map(top2[0])
            self.next_arr[0].encode_map(top2[0])

            self.tuple[5][1].encode_map(top2[1])
            self.next_arr[1].encode_map(top2[1])

            self.tuple[6][1].encode_map(bottom2[0])
            self.next_arr[2].encode_map(bottom2[0])

            self.tuple[7][1].encode_map(bottom2[1])
            self.next_arr[3].encode_map(bottom2[1])

            for i in self.next_arr:
                if i.get_non_attack() == total_non_attack:
                    return i


if __name__ == '__main__':
    G = Genetic(5)

    # G.choose_board()
    Gene = G.genetic_solver()
    print("Running Time:", G.get_runtime(), "ms")
    print("# of restart:", G.get_restarts())
    Gene.show()


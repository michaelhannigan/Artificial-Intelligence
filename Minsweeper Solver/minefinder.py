from mines import Mines
import time


class Sentence:
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def mark_mine(self, cell):
        if self.cells.__contains__(cell):
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if self.cells.__contains__(cell):
            self.cells.remove(cell)

    def __eq__(self, other):
        if self.cells == other.cells and self.count == other.count:
            return True
        return False

    def __str__(self):
        return f"{self.cells} = {self.count}"


class Solver2:
    def __init__(self, board_size, num_mines):
        self.board_size = board_size
        self.num_mines = num_mines
        self.m = Mines(self.board_size, self.num_mines)
        self.grid = self.m.checkcell((0, 0))
        self.m.showcurrent()
        self.sentence_list = []
        self.unmarked = []
        self.safe = set()
        self.safe_moves = []


    def sweep(self):
        self.__init_safe()
        self.__init_unmarked()
        #
        # before while loop
        #

        while not self.m.checkmines():

            self.__build_knowledge()

            for s1 in self.sentence_list:
                for s2 in self.sentence_list:
                    if s2.cells.issubset(s1.cells) and s2 != s1 and len(s2.cells) != 0:
                        new_cells = s1.cells.difference(s2.cells)
                        new_count = s1.count - s2.count
                        new_sentence = Sentence(new_cells, new_count)
                        if not self.sentence_list.__contains__(new_sentence):
                            self.sentence_list.append(new_sentence)

            # sets all cells in sentences to mines that have equal values to their count
            for sen in self.sentence_list:
                cells_copy = sen.cells.copy()
                if sen.count == len(cells_copy):
                    # self.sentence_list.remove(sen)
                    for cell in cells_copy:
                        sen.mark_mine(cell)
                        for s in self.sentence_list:
                            s.mark_mine(cell)
                        if not set(self.m.flags).__contains__(cell):
                            self.m.flags.append(cell)
                if sen.count == 0:
                    for cell in cells_copy:
                        if self.unmarked.__contains__(cell) and not set(self.m.flags).__contains__(cell):
                            self.safe_moves.append(cell)
                            sen.mark_safe(cell)
                            for s in self.sentence_list:
                                s.mark_safe(cell)

            if len(self.safe_moves) == 0:
                self.__make_random_move()

            #makes all the safe moves
            for m in self.safe_moves:
                self.__mark_safe(m)
                self.m.showcurrent()
            self.safe_moves = []

            self.m.showcurrent()

    def __make_random_move(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.grid[i][j] == ' ' and not set(self.m.flags).__contains__((i, j)):
                    self.__mark_safe((i, j))
                    print("MARKING SAFE:", (i, j))
                    self.m.showcurrent()
                    return

    def __mark_safe(self, cell):
        self.grid = self.m.checkcell(cell)
        self.safe.add(cell)
        self.unmarked.remove(cell)

    def __init_unmarked(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if not self.grid[i][j].isnumeric() and not set(self.m.flags).__contains__((i,j)):
                    self.unmarked.append((i, j))

    def __init_safe(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.grid[i][j].isnumeric():
                    self.safe.add((i, j))

    def __build_knowledge(self):
        self.sentence_list = []
        #goes through the grid and finds a number other than zero and creates a sentence from it
        for i in range(self.board_size):
            for j in range(self.board_size):
                added = False
                if self.grid[i][j] != "0" and self.grid[i][j] != ' ' and not set(self.m.flags).__contains__((i, j)):
                    added = True
                    tup = (i, j)
                    c_value = int(self.grid[tup[0]][tup[1]])
                    adj_set = self.__get_adj_set(tup)
                    new_sentence = Sentence(adj_set, c_value)
                    self.sentence_list.append(new_sentence)

                if j == self.board_size-1 and not added:
                    break

    def __get_adj_set(self, tup):
        #creates a set of all empty adjacent cells of tup

        x = tup[0]
        y = tup[1]
        adj_set = set()

        if x - 1 >= 0 and y - 1 >= 0:
            top_left = self.grid[x - 1][y - 1]
            if top_left == ' ':
                adj_set.add((x - 1, y - 1))

        if x - 1 >= 0:
            top_center = self.grid[x - 1][y]
            if top_center == ' ':
                adj_set.add((x - 1, y))

        if x - 1 >= 0 and y + 1 <= self.board_size - 1:
            top_right = self.grid[x - 1][y + 1]
            if top_right == ' ':
                adj_set.add((x - 1, y + 1))

        if y + 1 <= self.board_size - 1:
            middle_right = self.grid[x][y + 1]
            if middle_right == ' ':
                adj_set.add((x, y + 1))

        if x + 1 <= self.board_size - 1 and y + 1 <= self.board_size - 1:
            bottom_right = self.grid[x + 1][y + 1]
            if bottom_right == ' ':
                adj_set.add((x + 1, y + 1))

        if x + 1 <= self.board_size - 1:
            bottom_middle = self.grid[x + 1][y]
            if bottom_middle == ' ':
                adj_set.add((x + 1, y))

        if x + 1 <= self.board_size - 1:
            bottom_left = self.grid[x + 1][y - 1]
            if bottom_left == ' ':
                adj_set.add((x + 1, y - 1))

        if y - 1 >= 0:
            middle_left = self.grid[x][y - 1]
            if middle_left == ' ':
                adj_set.add((x, y - 1))

        return adj_set

if __name__ == '__main__':
    board_size = input("Enter the size of the board: ")
    num_mines = input("Enter the amount of mines: ")
    start_time = time.time()
    complete = False
    count = 1
    while not complete:
        try:
            board = Solver2(int(board_size), int(num_mines))
            board.sweep()
            complete = True
        except Exception as e:
            count += 1
    print("Board size: ", board_size, "X", board_size)
    print("Number of mines", num_mines)
    print("Program Runtime: ", time.time()-start_time, "seconds")
    print("Number of game restarts: ", count)
    print("Accuracy percentage: ", (1/count)*100, "%")


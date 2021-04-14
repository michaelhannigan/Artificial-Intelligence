from board import Board

if __name__ == '__main__':
    hill_climb = Board(5)
    hill_climb.fitness()
    hill_climb.hill_climb_solver()


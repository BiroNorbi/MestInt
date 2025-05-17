import heapq
import sys


class Move:
    def __init__(self, move, x, y, wx, wy):
        self.move = move
        self.x = x
        self.y = y
        self.wx = wx
        self.wy = wy

    def __str__(self):
        return f"Move: {self.move}, X: {self.x}, Y: {self.y} WallX: {self.wx}, WallY: {self.wy}"


class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.value = value

    def __lt__(self, other):
        return self.f < other.f

    def __str__(self):
        return f"Node: ({self.x}, {self.y}), F: {self.f}"


class PathFinding:
    def __init__(self, n):
        self.n = n
        self.board = [[Node(i, j, 0) for j in range(2 * self.n - 1)] for i in range(2 * self.n - 1)]
        self.visited = [[False for _ in range(2 * n - 1)] for _ in range(2 * n - 1)]
        self.path = []
        self.x = 0
        self.y = 0
        self.end_row = 0
        self.value = 0

    def clear_board(self, board):
        for i in range(2 * self.n - 1):
            for j in range(2 * self.n - 1):
                self.board[i][j].value = board[i][j]

    def heuristic(self, y):
        return abs(y - self.end_row)

    def set_entity(self, x, y, end_row, value):
        self.x = x
        self.y = y
        self.end_row = end_row
        self.value = value

    def get_neighbors(self, x, y):
        neighbors_dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for d in neighbors_dir:
            new_x = x + 2 * d[0]
            new_y = y + 2 * d[1]
            if 0 <= new_x < 2 * self.n - 1 and 0 <= new_y < 2 * self.n - 1:
                if self.board[x + d[0]][y + d[1]].value != 9:
                    neighbors.append(self.board[new_x][new_y])
                value = self.board[new_x][new_y].value
                if value != 0 and value != self.value:
                    if 1 <= new_x + d[0] < 2 * self.n - 1 and 1 <= new_y + d[1] < 2 * self.n - 1 and \
                            self.board[new_x + d[0]][new_y + d[1]].value != 9:
                        neighbors.append(self.board[new_x][new_y])
                    else:
                        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        for ed in directions:
                            enemy_x = new_x + 2 * ed[0]
                            enemy_y = new_y + 2 * ed[1]

                            if 0 <= enemy_x < 2 * self.n - 1 and 0 <= enemy_y < 2 * self.n - 1:
                                if self.board[enemy_x][enemy_y] == 0 and self.board[new_x + ed[0]][new_y + ed[1]] != 9:
                                    neighbors.append(self.board[enemy_x][enemy_y])

        return neighbors

    def a_star(self):
        start = Node(self.x, self.y, 1)
        open_queue = [start]
        open_dict = {start: True}
        closed_set = {}

        start.g = 0
        start.h = self.heuristic(start.y)
        start.f = start.g + start.h

        while open_queue:
            current = heapq.heappop(open_queue)
            if current.y == self.end_row:
                return True

            closed_set[current] = True

            neighbors = self.get_neighbors(current.x, current.y)

            for neighbor in neighbors:
                if neighbor in closed_set:
                    continue

                g = current.g + 1

                if neighbor not in open_dict:
                    neighbor.parent = current
                    neighbor.g = g
                    neighbor.h = self.heuristic(neighbor.y)
                    neighbor.f = g + neighbor.h

                    heapq.heappush(open_queue, neighbor)
                    open_dict[neighbor] = True
                elif g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = g
                    neighbor.f = g + neighbor.h
                    heapq.heapify(open_queue)

        return False


class Quoridor:
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.walls = []
        self.enemy_last_move = None
        self.player_pos = None
        self.enemy_pos = None
        self.n = 0
        self.m = 0
        self.board = None
        self.game_over = False
        self.winner = None
        self.path_finding = None

    def get_player_pos(self):
        return self.player_pos.x, self.player_pos.y

    def print_board(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[2 * i][2 * j], end=" ")
            print()

    def update_board(self):
        for i in range(2 * self.n - 1):
            line = sys.stdin.readline().strip().split(" ")
            for j in range(2 * self.n - 1):
                self.board[i][j] = int(line[j])

                if int(line[j]) == 1:
                    self.player_pos = Node(i, j, 1)
                if int(line[j]) == 2:
                    self.enemy_pos = Node(i, j, 2)

    def read_board_from_console(self):
        first = sys.stdin.readline().strip().split(" ")
        self.n = int(first[0])
        self.m = int(first[1])
        self.board = [[0 for _ in range(2 * self.n - 1)] for _ in range(2 * self.m - 1)]

        self.path_finding = PathFinding(self.n)
        self.update_board()
        self.print_board()

    def read_board_from_file(self):
        with open("board_input.txt", "r") as f:
            first = f.readline().strip().split(" ")
            self.n = int(first[0])
            self.m = int(first[1])
            self.board = [[0 for _ in range(2 * self.n - 1)] for _ in range(2 * self.m - 1)]

            self.path_finding = PathFinding(self.n)
            for i in range(2 * self.n - 1):
                line = f.readline().strip().split(" ")
                for j in range(2 * self.n - 1):
                    self.board[i][j] = int(line[j])

                    if int(line[j]) == 1:
                        self.player_pos = Node(i, j, 1)
                    if int(line[j]) == 2:
                        self.enemy_pos = Node(i, j, 2)

    def read_board(self, console=True):
        if console:
            self.read_board_from_console()
        else:
            self.read_board_from_file()

    def read_enemy_step(self):
        enemy_step = sys.stdin.readline().strip().split(" ")

        if len(enemy_step) == 3:
            wx = None
            wy = None
        else:
            wy = int(enemy_step[3])
            wx = int(enemy_step[4])

        self.enemy_last_move = Move(enemy_step[0], int(enemy_step[2]), int(enemy_step[1]), wx, wy)
        self.update_board()

    def is_game_over(self):
        for j in range(self.n):
            if self.board[0][j] == 1:
                return 1

        for j in range(self.n):
            if self.board[2 * self.n - 2][j] == 1:
                return -1

        return 0

    def wall_can_be_placed(self, x1, y1, x2, y2):
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2

        if self.path_finding.board[x1][y1].value == 0 and self.path_finding.board[mid_x][mid_y].value == 0 and \
                self.path_finding.board[x2][y2].value == 0:
            self.path_finding.board[x1][y1].value = 9
            self.path_finding.board[x2][y2].value = 9
            self.path_finding.board[mid_x][mid_y].value = 9

            self.path_finding.set_entity(self.player_pos.x, self.player_pos.y, 0, 1)
            path1 = self.path_finding.a_star()
            self.path_finding.set_entity(self.enemy_pos.x, self.enemy_pos.y, 2 * self.n - 2, 2)
            path2 = self.path_finding.a_star()

            self.path_finding.board[x1][y1].value = 0
            self.path_finding.board[x2][y2].value = 0
            self.path_finding.board[mid_x][mid_y].value = 0

            return path1 and path2
        else:
            return False

    def get_all_possible_moves(self, x, y):
        possible_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d in directions:
            new_x = x + 2 * d[0]
            new_y = y + 2 * d[1]
            if 0 <= new_x < 2 * self.n - 1 and 0 <= new_y < 2 * self.n - 1:
                if self.board[x + d[0]][y + d[1]] != 9:
                    if self.board[new_x][new_y] == 0:
                        possible_moves.append(Move("L", new_x, new_y, None, None))
                    elif self.board[new_x][new_y] == 2:
                        for ed in directions:
                            enemy_x = new_x + 2 * ed[0]
                            enemy_y = new_y + 2 * ed[1]

                            if 0 <= enemy_x < 2 * self.n - 1 and 0 <= enemy_y < 2 * self.n - 1:
                                if self.board[enemy_x][enemy_y] == 0 and self.board[new_x + ed[0]][new_y + ed[1]] != 9:
                                    possible_moves.append(Move("L", enemy_x, enemy_y, None, None))
        self.path_finding.clear_board(self.board)

        for i in range(self.n - 1):
            for j in range(self.n - 1):
                x = 2 * i + 1
                y = 2 * j
                if self.wall_can_be_placed(x, y, x, y + 2):
                    possible_moves.append(Move("F", x, y, x, y + 2))

        for j in range(self.n - 1):
            for i in range(self.n - 1):
                x = 2 * i
                y = 2 * j + 1
                if self.wall_can_be_placed(x, y, x + 2, y):
                    possible_moves.append(Move("F", x, y, x + 2, y))

        return possible_moves


def main():
    quoridor = Quoridor()
    quoridor.read_board(console=False)
    board = quoridor.board.copy()
    (x, y) = quoridor.get_player_pos()
    possible_moves = quoridor.get_all_possible_moves(x, y)
    for moves in possible_moves:
        print(moves)

        if moves.move == "L":
            board[x][y] = 0
            board[moves.x][moves.y] = 1
            print()
            for i in range(2 * quoridor.n - 1):
                for j in range(2 * quoridor.n - 1):
                    print(board[i][j], end=" ")
                print()
            print()
            board[x][y] = 1
            board[moves.x][moves.y] = 0
        else:
            mid_x = (moves.x + moves.wx) // 2
            mid_y = (moves.y + moves.wy) // 2
            board[moves.x][moves.y] = 9
            board[moves.wx][moves.wy] = 9
            board[mid_x][mid_y] = 9
            print()
            for i in range(2 * quoridor.n - 1):
                for j in range(2 * quoridor.n - 1):
                    print(board[i][j], end=" ")
                print()
            print()

            board[moves.x][moves.y] = 0
            board[moves.wx][moves.wy] = 0
            board[mid_x][mid_y] = 0


if __name__ == "__main__":
    main()

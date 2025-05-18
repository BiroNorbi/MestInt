import heapq
import sys
import time


class Move:
    def __init__(self, move, x, y, wx, wy):
        self.move = move
        self.x = x
        self.y = y
        self.wx = wx
        self.wy = wy

    def __str__(self):
        return f"Move: {self.move}, X: {self.x}, Y: {self.y} WallX: {self.wx}, WallY: {self.wy}"

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move == other.move and self.x == other.x and self.y == other.y and self.wx == other.wx and \
                   self.wy == other.wy
        return False

    def __hash__(self):
        return hash((self.move, self.x, self.y, self.wx, self.wy))

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

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


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
        self.last = None

    def update_board(self, board):
        for i in range(2 * self.n - 1):
            for j in range(2 * self.n - 1):
                self.board[i][j].value = board[i][j]

    def heuristic(self, x):
        return abs(x - self.end_row)

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
            if 0 <= new_x < 2 * self.n - 1 and 0 <= new_y < 2 * self.n - 1 and self.board[x + d[0]][
                y + d[1]].value != 9:
                if self.board[new_x][new_y].value == 0:
                    neighbors.append(Node(new_x, new_y, 0))
                else:
                    if 0 < new_x + d[0] < 2 * self.n - 1 and 0 < new_y + d[1] < 2 * self.n - 1 and \
                            self.board[new_x + d[0]][new_y + d[1]].value != 9:
                        neighbors.append(Node(new_x + 2 * d[0], new_y + 2 * d[1], 0))
                    else:
                        for ed in neighbors_dir:
                            enemy_x = new_x + 2 * ed[0]
                            enemy_y = new_y + 2 * ed[1]

                            if 0 <= enemy_x < 2 * self.n - 1 and 0 <= enemy_y < 2 * self.n - 1 and self.board[enemy_x][enemy_y].value == 0 and \
                                    self.board[new_x + ed[0]][new_y + ed[1]].value != 9:
                                neighbors.append(Node(new_x, new_y, 0))
                                break

        return neighbors

    def a_star(self):
        start = Node(self.x, self.y, self.value)
        open_queue = [start]
        open_dict = {start: True}
        closed_set = {}

        start.g = 0
        start.h = self.heuristic(start.x)
        start.f = start.g + start.h

        while open_queue:
            current = heapq.heappop(open_queue)
            self.last = current

            if current.x == self.end_row:
                return True, current.g

            closed_set[current] = True

            neighbors = self.get_neighbors(current.x, current.y)

            for neighbor in neighbors:
                if neighbor in closed_set:
                    continue

                g = current.g + 1

                if neighbor not in open_dict:
                    neighbor.parent = current
                    neighbor.g = g
                    neighbor.h = self.heuristic(neighbor.x)
                    neighbor.f = g + neighbor.h

                    heapq.heappush(open_queue, neighbor)
                    open_dict[neighbor] = True
                elif g < neighbor.g:
                    neighbor.parent = current
                    neighbor.g = g
                    neighbor.f = g + neighbor.h
                    heapq.heapify(open_queue)
        return False, float('inf')


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
        self.player_walls = 0
        self.enemy_walls = 0

    def get_player_pos(self):
        return self.player_pos.x, self.player_pos.y

    def get_enemy_pos(self):
        return self.enemy_pos.x, self.enemy_pos.y

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
        self.player_pos = self.m

        self.path_finding = PathFinding(self.n)
        self.update_board()
        self.print_board()

    def read_board_from_file(self):
        with open("board_input.txt", "r") as f:
            first = f.readline().strip().split(" ")
            self.n = int(first[0])
            self.m = int(first[1])
            self.board = [[0 for _ in range(2 * self.n - 1)] for _ in range(2 * self.m - 1)]
            self.player_pos = self.m

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

    def is_game_over(self, board):
        for j in range(self.n):
            if board[0][j] == 1:
                return 1

        for j in range(self.n):
            if board[2 * self.n - 2][j] == 2:
                return -1

        return 0

    def wall_can_be_placed(self, x1, y1, x2, y2, walls_left):
        if walls_left == 0:
            False, float('inf'), float('inf')

        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2

        if self.path_finding.board[x1][y1].value == 0 and self.path_finding.board[mid_x][mid_y].value == 0 and \
                self.path_finding.board[x2][y2].value == 0:
            self.path_finding.board[x1][y1].value = 9
            self.path_finding.board[x2][y2].value = 9
            self.path_finding.board[mid_x][mid_y].value = 9

            self.path_finding.set_entity(self.player_pos.x, self.player_pos.y, 0, 1)
            path1, player_distance = self.path_finding.a_star()
            self.path_finding.set_entity(self.enemy_pos.x, self.enemy_pos.y, 2 * self.n - 2, 2)
            path2, enemy_distance = self.path_finding.a_star()

            self.path_finding.board[x1][y1].value = 0
            self.path_finding.board[x2][y2].value = 0
            self.path_finding.board[mid_x][mid_y].value = 0

            return path1 and path2, player_distance, enemy_distance
        else:
            return False, float('inf'), float('inf')

    def move(self, x, y, new_x, new_y, player, board):
        self.path_finding.set_entity(new_x, new_y, 0 if player == 1 else 2 * self.n - 2, player)
        board[new_x][new_y] = player
        board[x][y] = 0

        self.path_finding.update_board(board)

        path, player_distance = self.path_finding.a_star()

        board[new_x][new_y] = 0
        board[x][y] = player

        return path, player_distance

    def get_all_possible_moves(self, x, y, player, enemy, board):
        possible_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        self.path_finding.set_entity(enemy.x, enemy.y, 0 if player else 2 * self.n - 2, 1 if player else 2)
        _, enemy_distance = self.path_finding.a_star()
        p = 1 if player else 2

        for d in directions:
            new_x = x + 2 * d[0]
            new_y = y + 2 * d[1]
            if 0 <= new_x < 2 * self.n - 1 and 0 <= new_y < 2 * self.n - 1 and board[x + d[0]][y + d[1]] != 9:
                if board[new_x][new_y] == 0:
                    path, player_distance = self.move(x, y, new_x, new_y, p, board)

                    possible_moves.append((Move("L", new_x, new_y, None, None), player_distance if player else enemy_distance, enemy_distance if player else player_distance))
                else:
                    if 0 < new_x + 2 * d[0] < 2 * self.n - 1 and 0 < new_y + 2 * d[1] < 2 * self.n - 1 and \
                            self.board[new_x + d[0]][new_y + d[1]] != 9:
                        path, player_distance = self.move(x, y, new_x + 2 * d[0], new_y + 2 * d[1], p, board)

                        possible_moves.append(
                            (Move("L", new_x, new_y, None, None), player_distance if player else enemy_distance, enemy_distance if player else player_distance))
                    else:
                        for ed in directions:
                            enemy_x = new_x + 2 * ed[0]
                            enemy_y = new_y + 2 * ed[1]

                            if 2 * self.n - 1 > enemy_x >= 0 == board[enemy_x][
                                enemy_y] and 0 <= enemy_y < 2 * self.n - 1 and \
                                    self.board[new_x + ed[0]][new_y + ed[1]] != 9:
                                path, player_distance = self.move(x, y, enemy_x, enemy_y, p, board)

                                possible_moves.append(
                                    (Move("L", new_x, new_y, None, None), player_distance, enemy_distance))
                                break

        self.path_finding.update_board(board)

        for i in range(self.n - 1):
            for j in range(self.n - 1):
                x = 2 * i + 1
                y = 2 * j
                wall_can_be_placed, player_distance, enemy_distance = self.wall_can_be_placed(x, y, x, y + 2,
                                                                                              self.player_walls)
                if wall_can_be_placed:
                    possible_moves.append((Move("F", x, y, x, y + 2), player_distance, enemy_distance))

        for j in range(self.n - 1):
            for i in range(self.n - 1):
                x = 2 * i
                y = 2 * j + 1
                wall_can_be_placed, player_distance, enemy_distance = self.wall_can_be_placed(x, y, x + 2, y,
                                                                                              self.player_walls)
                if wall_can_be_placed:
                    possible_moves.append((Move("F", x, y, x + 2, y), player_distance, enemy_distance))

        return possible_moves

    def heuristic(self, minimum, maximum, a=1):
        return -1 * (maximum - a * minimum)

    def min_max(self, board, player, player_pos, enemy_pos, player_walls, enemy_walls, max_depth=5, depth=0):
        label = self.is_game_over(board)
        if label != 0:
            return (float('inf'), None) if label == 1 else (-float('inf'), None)

        if depth >= max_depth:
            self.path_finding.set_entity(player_pos.x, player_pos.y, 0, 1)
            _, player_distance = self.path_finding.a_star()
            self.path_finding.set_entity(enemy_pos.x, enemy_pos.y, 2 * self.n - 2, 2)
            _, enemy_distance = self.path_finding.a_star()
            label = self.heuristic(enemy_distance, player_distance)
            return label, None

        best_value = -float('inf') if player else float('inf')
        best_move = None

        (x, y) = (player_pos.x, player_pos.y) if player else (enemy_pos.x, enemy_pos.y)

        possible_moves = self.get_all_possible_moves(x, y, player, player_pos if player else enemy_pos, board)

        for move, player_d, enemy_d in possible_moves:
            # print(depth, move, player_d, enemy_d)
            original_value = board[x][y]

            if move.move == "L":
                board[x][y] = 0
                board[move.x][move.y] = 1 if player else 2
            else:
                board[move.x][move.y] = 9
                board[move.wx][move.wy] = 9
                board[((move.wx + move.x) // 2)][(move.wy + move.y) // 2] = 9

            if move.move == "L":
                if player:
                    player_pos.x, player_pos.y = move.x, move.y
                else:
                    enemy_pos.x, enemy_pos.y = move.x, move.y

            value, _ = self.min_max(board, not player, player_pos, enemy_pos, player_walls, enemy_walls, max_depth,
                                    depth + 1)

            if move.move == "L":
                board[x][y] = original_value
                board[move.x][move.y] = 0
            else:
                board[move.x][move.y] = 0
                board[move.wx][move.wy] = 0
                board[((move.wx + move.x) // 2)][(move.wy + move.y) // 2] = 0

            if move.move == "L":
                if player:
                    player_pos.x, player_pos.y = x, y
                else:
                    enemy_pos.x, enemy_pos.y = x, y

            if (player and value >= best_value) or (not player and value <= best_value):
                best_value = value
                best_move = move

        return best_value, best_move


def main():
    quoridor = Quoridor()
    quoridor.read_board(console=False)
    board = quoridor.board.copy()
    (x, y) = quoridor.get_player_pos()
    # possible_moves = quoridor.get_all_possible_moves(x, y, quoridor.enemy_pos, board)
    # board = [
    #     [0, 0, 0, 0, 2, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 9, 9, 9, 0, 0],
    #     [0, 0, 1, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ]
    #
    # path_finding = PathFinding(5)
    # path_finding.update_board(board)
    # path_finding.set_entity(0, 4, 8, 2)
    # path, player = path_finding.a_star()
    # current = path_finding.last
    #
    # while current != None:
    #     print(current)
    #     current = current.parent
    #
    # print(path, player)
    # for move, player, enemy in possible_moves:
    #     print(f"""
    #     Move: {move}
    #     Player distance: {player}
    #     Enemy distance: {enemy}""")
    #
    #     if move.move == "L":
    #         board[x][y] = 0
    #         board[move.x][move.y] = 1
    #         print()
    #         for i in range(2 * quoridor.n - 1):
    #             for j in range(2 * quoridor.n - 1):
    #                 print(board[i][j], end=" ")
    #             print()
    #         print()
    #         board[x][y] = 1
    #         board[move.x][move.y] = 0
    #     else:
    #         mid_x = (move.x + move.wx) // 2
    #         mid_y = (move.y + move.wy) // 2
    #         board[move.x][move.y] = 9
    #         board[move.wx][move.wy] = 9
    #         board[mid_x][mid_y] = 9
    #         print()
    #         for i in range(2 * quoridor.n - 1):
    #             for j in range(2 * quoridor.n - 1):
    #                 print(board[i][j], end=" ")
    #             print()
    #         print()
    #
    #         board[move.x][move.y] = 0
    #         board[move.wx][move.wy] = 0
    #         board[mid_x][mid_y] = 0
    start = time.time()
    label, best_move = quoridor.min_max(board, True, quoridor.player_pos, quoridor.enemy_pos,
                                       quoridor.player_walls, quoridor.enemy_walls, max_depth=3)
    end = time.time()

    print("Time taken:", end - start)
    print(label, best_move)


if __name__ == "__main__":
    main()

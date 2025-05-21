import heapq
import sys
import time

import numpy as np
import logging

logging.basicConfig(
    filename='game_debug.log',           # Log file name
    filemode='w',                        # Overwrite on each run, use 'a' to append
    level=logging.DEBUG,                 # Log everything (DEBUG and above)
    format='%(asctime)s - %(levelname)s - %(message)s'
)


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

    def __copy__(self):
        new_node = Node(self.x, self.y, self.value)
        new_node.g = self.g
        new_node.h = self.h
        new_node.f = self.f
        new_node.parent = self.parent
        return new_node


class PathFinding:
    def __init__(self, n):
        self.n = n
        self.board = np.array([[Node(i, j, 0) for j in range(2 * self.n - 1)] for i in range(2 * self.n - 1)],
                              dtype=object)
        self.path = []
        self.x = 0
        self.y = 0
        self.end_row = 0
        self.value = 0
        self.last = None
        self.path_cache = {}

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

                            if 0 <= enemy_x < 2 * self.n - 1 and 0 <= enemy_y < 2 * self.n - 1 and self.board[enemy_x][
                                enemy_y].value == 0 and \
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
        self.level = 0
        self.player_goal = 0
        self.enemy_goal = 0

    def get_player_pos(self):
        return self.player_pos.x, self.player_pos.y

    def get_enemy_pos(self):
        return self.enemy_pos.x, self.enemy_pos.y

    def print_board(self):
        for i in range(self.n):
            for j in range(self.n):
                print(self.board[2 * i][2 * j], end=" ")
            print()

    def update_board(self, check_enemy_walls=False):
        for i in range(2 * self.n - 1):
            line = sys.stdin.readline().strip().split(" ")
            for j in range(2 * self.n - 1):
                self.board[i][j] = int(line[j])

                if check_enemy_walls and int(line[j]) == 9:
                    self.enemy_walls = self.m - 1

                if int(line[j]) == 1:
                    self.player_pos = Node(i, j, 1)
                if int(line[j]) == 2:
                    self.enemy_pos = Node(i, j, 2)

    def read_board_from_console(self):
        first = sys.stdin.readline().strip().split(" ")
        self.n = int(first[0])
        self.m = int(first[1])
        self.board = np.zeros((2 * self.n - 1, 2 * self.n - 1), dtype=int)
        self.player_walls = self.m

        self.path_finding = PathFinding(self.n)
        self.update_board(check_enemy_walls=True)

    def read_board_from_file(self):
        with open("board_input.txt", "r") as f:
            first = f.readline().strip().split(" ")
            self.n = int(first[0])
            self.m = int(first[1])
            self.board = np.zeros((2 * self.n - 1, 2 * self.n - 1), dtype=int)
            self.player_pos = self.m

            self.path_finding = PathFinding(self.n)
            for i in range(2 * self.n - 1):
                line = f.readline().strip().split(" ")
                for j in range(2 * self.n - 1):
                    self.board[i][j] = int(line[j])

                    if int(line[j]) == 9:
                        self.enemy_walls = self.m - 1

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
            self.enemy_walls -= 1

        self.enemy_last_move = Move(enemy_step[0], int(enemy_step[2]), int(enemy_step[1]), wx, wy)
        self.update_board()

    def is_game_over(self, board):
        for j in range(self.n):
            if board[self.player_goal][j] == 1:
                return 1

        for j in range(self.n):
            if board[self.enemy_goal][j] == 2:
                return -1

        return 0

    def check_if_valid_move(self, board, move, position, value, walls):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        if move.move == "L":
            for d in directions:
                new_x = position.x + 2 * d[0]
                new_y = position.y + 2 * d[1]
                if 0 <= new_x < 2 * self.n - 1 and 0 <= new_y < 2 * self.n - 1 and board[position.x + d[0]][
                    position.y + d[1]] != 9:
                    if board[new_x][new_y] == 0:
                        if new_x == move.x and new_y == move.y:
                            return True
                    else:
                        if 0 <= new_x + 2 * d[0] < 2 * self.n - 1 and 0 <= new_y + 2 * d[1] < 2 * self.n - 1 and \
                                board[new_x + d[0]][new_y + d[1]] != 9 and new_x + 2 * d[0] == move.x and new_y + 2 * d[
                            1] == move.y:
                            return True
                        else:
                            for ed in directions:
                                enemy_x = new_x + 2 * ed[0]
                                enemy_y = new_y + 2 * ed[1]

                                if 2 * self.n - 1 > enemy_x >= 0 and 0 <= enemy_y < 2 * self.n - 1 and 0 == board[enemy_x][enemy_y] and \
                                        board[new_x + ed[0]][new_y + ed[1]] != 9 and enemy_x == move.x and enemy_y == move.y:
                                    return True
        else:
            wall_can_be_placed, _, _ = self.wall_can_be_placed(move.x, move.y, move.wx, move.wy, walls)
            return wall_can_be_placed

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

            self.path_finding.set_entity(self.player_pos.x, self.player_pos.y, self.player_goal, 1)
            path1, player_distance = self.path_finding.a_star()
            self.path_finding.set_entity(self.enemy_pos.x, self.enemy_pos.y, self.enemy_goal, 2)
            path2, enemy_distance = self.path_finding.a_star()

            self.path_finding.board[x1][y1].value = 0
            self.path_finding.board[x2][y2].value = 0
            self.path_finding.board[mid_x][mid_y].value = 0

            return path1 and path2, player_distance, enemy_distance
        else:
            return False, float('inf'), float('inf')

    def move(self, x, y, new_x, new_y, player, board):
        self.path_finding.set_entity(new_x, new_y, self.player_goal if player == 1 else self.enemy_goal, player)

        self.path_finding.board[new_x][new_y].value = player
        self.path_finding.board[x][y].value = 0

        path, player_distance = self.path_finding.a_star()

        return path, player_distance

    def get_all_possible_moves(self, x, y, player, enemy, board, walls_left):
        possible_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        enemy_goal = self.enemy_goal if player else self.player_goal
        enemy_id = 2 if player else 1
        self.path_finding.set_entity(enemy.x, enemy.y, enemy_goal, enemy_id)
        _, enemy_distance = self.path_finding.a_star()

        p = 1 if player else 2

        for d in directions:
            dx, dy = d
            mid_x, mid_y = x + dx, y + dy
            new_x, new_y = x + 2 * dx, y + 2 * dy

            if 0 <= mid_x < 2 * self.n - 1 and 0 <= mid_y < 2 * self.n - 1 and board[mid_x][mid_y] != 9:
                if 0 <= new_x < 2 * self.n - 1 and 0 <= new_y < 2 * self.n - 1:
                    if board[new_x][new_y] == 0:
                        path, player_distance = self.move(x, y, new_x, new_y, p, board)
                        possible_moves.append((Move("L", new_x, new_y, None, None),
                                               player_distance if player else enemy_distance,
                                               enemy_distance if player else player_distance))
                    elif board[new_x][new_y] in [1, 2]:
                        jump_x, jump_y = new_x + 2 * dx, new_y + 2 * dy
                        jump_mid_x, jump_mid_y = new_x + dx, new_y + dy
                        if 0 <= jump_mid_x < 2 * self.n - 1 and 0 <= jump_mid_y < 2 * self.n - 1 and board[jump_mid_x][
                            jump_mid_y] != 9:
                            if 0 <= jump_x < 2 * self.n - 1 and 0 <= jump_y < 2 * self.n - 1:
                                path, player_distance = self.move(x, y, jump_x, jump_y, p, board)
                                possible_moves.append((Move("L", jump_x, jump_y, None, None),
                                                       player_distance if player else enemy_distance,
                                                       enemy_distance if player else player_distance))
                        else:
                            for ed in directions:
                                ex, ey = new_x + 2 * ed[0], new_y + 2 * ed[1]
                                between_x, between_y = new_x + ed[0], new_y + ed[1]
                                if 0 <= ex < 2 * self.n - 1 and 0 <= ey < 2 * self.n - 1 and board[ex][ey] == 0:
                                    if board[between_x][between_y] != 9:
                                        path, player_distance = self.move(x, y, ex, ey, p, board)
                                        possible_moves.append((Move("L", ex, ey, None, None),
                                                               player_distance, enemy_distance))
                                        break

        if walls_left > 0:
            for i in range(self.n - 1):
                for j in range(self.n - 1):
                    x = 2 * i + 1
                    y = 2 * j
                    wall_can_be_placed, player_distance, enemy_distance = self.wall_can_be_placed(x, y, x, y + 2,
                                                                                                  walls_left)
                    if wall_can_be_placed:
                        possible_moves.append((Move("F", x, y, x, y + 2), player_distance, enemy_distance))

            for j in range(self.n - 1):
                for i in range(self.n - 1):
                    x = 2 * i
                    y = 2 * j + 1
                    wall_can_be_placed, player_distance, enemy_distance = self.wall_can_be_placed(x, y, x + 2, y,
                                                                                                  walls_left)
                    if wall_can_be_placed:
                        possible_moves.append((Move("F", x, y, x + 2, y), player_distance, enemy_distance))

        return possible_moves

    def heuristic(self, minimum, maximum, a=1):
        return -1 * (maximum - a * minimum)

    def min_max(self, board, player, player_pos, enemy_pos,
                player_walls, enemy_walls, max_depth=5, depth=0,
                alpha=-float('inf'), beta=float('inf')):
        logging.info(
f"""
Board:
{board}
Player: {player_pos}
Enemy: {enemy_pos}
Player walls: {player_walls}
enemy walls: {enemy_walls}
Depth: {depth}
Alpha: {alpha}
Beta: {beta}
""")
        label = self.is_game_over(board)
        if label != 0:
            return (float('inf'), None) if label == 1 else (-float('inf'), None)

        if depth >= max_depth:
            self.path_finding.set_entity(player_pos.x, player_pos.y, self.player_goal, 1)
            _, player_distance = self.path_finding.a_star()
            self.path_finding.set_entity(enemy_pos.x, enemy_pos.y, self.enemy_goal, 2)
            _, enemy_distance = self.path_finding.a_star()
            score = self.heuristic(enemy_distance, player_distance)
            return score, None

        best_move = None
        best_value = -float('inf') if player else float('inf')
        (x, y) = (player_pos.x, player_pos.y) if player else (enemy_pos.x, enemy_pos.y)

        moves = self.get_all_possible_moves(x, y, player, enemy_pos if player else player_pos, board, player_walls if player else enemy_walls)
        logging.info(f"Moves: {moves}")
        for move, player_d, enemy_d in moves:
            new_board = board.copy()
            new_player_pos = Node(player_pos.x, player_pos.y, 1)
            new_enemy_pos = Node(enemy_pos.x, enemy_pos.y, 2)

            if move.move == "L":
                new_board[x][y] = 0
                new_board[move.x][move.y] = 1 if player else 2
                if player:
                    new_player_pos.x, new_player_pos.y = move.x, move.y
                else:
                    new_enemy_pos.x, new_enemy_pos.y = move.x, move.y
            else:
                new_board[move.x][move.y] = 9
                new_board[move.wx][move.wy] = 9
                new_board[(move.x + move.wx) // 2][(move.y + move.wy) // 2] = 9

            value, _ = self.min_max(new_board,
                                    not player,
                                    new_player_pos,
                                    new_enemy_pos,
                                    player_walls - 1 if move.move == "F" and player else player_walls,
                                    enemy_walls - 1 if move.move == "F" and not player else enemy_walls,
                                    max_depth,
                                    depth + 1,
                                    alpha,
                                    beta)

            if player:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)

            if beta <= alpha:
                break

        if player and best_value == -float('inf'):
            best_move = moves[0][0]
            best_value = moves[0][1]
        elif not player and best_value == float('inf'):
            best_move = moves[0][0]
            best_value = moves[0][2]

        return best_value, best_move


def main():
    quoridor = Quoridor()
    quoridor.read_board(console=False)

    while quoridor.is_game_over(quoridor.board) == 0:
        start = time.time()
        _, move = quoridor.min_max(quoridor.board, True, quoridor.player_pos, quoridor.enemy_pos, quoridor.m,
                                   quoridor.m, max_depth=3)

        end = time.time()
        # moves = quoridor.get_all_possible_moves(quoridor.player_pos.x, quoridor.player_pos.y, True,
        #                                 quoridor.enemy_pos, quoridor.board, quoridor.player_walls)
        # for m in moves:
        #     print(m[0], m[1], m[2])
        print("Time taken:", end - start)
        print("Level:", quoridor.level)
        if move.move == "L":
            quoridor.board[quoridor.player_pos.x][quoridor.player_pos.y] = 0
            quoridor.board[move.x][move.y] = 1
            print(f"L {move.y} {move.x}")
        else:
            quoridor.board[move.x][move.y] = 9
            quoridor.board[move.wx][move.wy] = 9
            quoridor.board[(move.x + move.wx) // 2][(move.y + move.wy) // 2] = 9
            quoridor.player_walls -= 1
            print(f"F {move.y} {move.x} {move.wy} {move.wx}")

        quoridor.read_enemy_step()


if __name__ == "__main__":
    main()

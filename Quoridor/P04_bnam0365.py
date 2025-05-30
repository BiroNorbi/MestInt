import os
import time

import numpy as np

from L04_bnam0365 import Quoridor, Node, PathFinding, Move


class QuoridorUI:
    LOGO = r"""
     ________  ___  ___  ________  ________  ___  ________  ________  ________     
    |\   __  \|\  \|\  \|\   __  \|\   __  \|\  \|\   ___ \|\   __  \|\   __  \    
    \ \  \|\  \ \  \\\  \ \  \|\  \ \  \|\  \ \  \ \  \_|\ \ \  \|\  \ \  \|\  \   
     \ \  \\\  \ \  \\\  \ \  \\\  \ \   _  _\ \  \ \  \ \\ \ \  \\\  \ \   _  _\  
      \ \  \\\  \ \  \\\  \ \  \\\  \ \  \\  \\ \  \ \  \_\\ \ \  \\\  \ \  \\  \| 
       \ \_____  \ \_______\ \_______\ \__\\ _\\ \__\ \_______\ \_______\ \__\\ _\ 
        \|___| \__\|_______|\|_______|\|__|\|__|\|__|\|_______|\|_______|\|__|\|__|
              \|__|                                                                
    """

    PLAYER_WINS = r"""
        ____  __                                  _           
   / __ \/ /___ ___  _____  _____   _      __(_)___  _____
  / /_/ / / __ `/ / / / _ \/ ___/  | | /| / / / __ \/ ___/
 / ____/ / /_/ / /_/ /  __/ /      | |/ |/ / / / / (__  ) 
/_/   /_/\__,_/\__, /\___/_/       |__/|__/_/_/ /_/____/  
              /____/                                      
    """
    ENEMY_WINS = r"""
        ____        __              _           
   / __ )____  / /_   _      __(_)___  _____
  / __  / __ \/ __/  | | /| / / / __ \/ ___/
 / /_/ / /_/ / /_    | |/ |/ / / / / (__  ) 
/_____/\____/\__/    |__/|__/_/_/ /_/____/  
    """

    YOUR_TURN = "Your turn"
    ENEMY_TURN = "Enemy turn"

    def __init__(self):
        self.board = None
        self.game = Quoridor()
        self.terminal_width = self.get_terminal_width()
        self.terminal_height = self.get_terminal_height()
        self.board_size = 3
        self.player_name = "Player"
        self.pending = " " * (self.terminal_width // 4)
        self.number_of_walls = 5
        self.player_walls = 5
        self.enemy_walls = 5
        self.player_pos = None
        self.enemy_pos = None
        self.player_ui_pos = None
        self.player_goal_row = 0
        self.enemy_goal_row = 0

    @staticmethod
    def get_terminal_width():
        return os.get_terminal_size().columns

    @staticmethod
    def get_terminal_height():
        return os.get_terminal_size().lines

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def center_text(self, text):
        return text.center(self.terminal_width)

    def display_logo(self):
        self.clear_screen()
        parts = self.LOGO.split("\n")

        for p in parts:
            print(self.center_text(p))

        time.sleep(1.3)

    def get_reverse_board(self, board):
        if board is None:
            return None
        return np.flipud(board)

    def move(self, move, position, value):
        if move.move == "L":
            val = self.board[position.x][position.y]
            self.board[position.x][position.y] = 0
            self.board[move.x][move.y] = val

        else:
            self.board[move.x][move.y] = 9
            self.board[(move.x + move.wx) // 2][(move.y + move.wy) // 2] = 9
            self.board[move.wx][move.wy] = 9

    def get_player_input(self):
        self.clear_screen()
        print(self.center_text("Welcome to Quoridor!"))
        print()

        print(f"{self.pending}Enter your name: ", end="")
        self.player_name = input().strip()
        while not self.player_name:
            print(f"{self.pending}Name cannot be empty!")
            print(f"{self.pending}Enter your name: ", end="")
            self.player_name = input().strip()

        while True:
            try:
                print(f"{self.pending}Enter the board size (an odd number between 3 and 9): ", end="")
                self.board_size = int(input())
                if 3 <= self.board_size <= 10 and self.board_size % 2 == 1:
                    break
                print(f"{self.pending}Please enter an odd number between 3 and 9")
            except ValueError:
                print(f"{self.pending}Please enter a valid number")

        self.board = np.zeros((2 * self.board_size - 1, 2 * self.board_size - 1), dtype=int)
        self.board[0][(2 * self.board_size - 1) // 2] = 1
        self.board[2 * self.board_size - 2][(2 * self.board_size - 1) // 2] = 2
        self.player_pos = Node(0, (2 * self.board_size - 1) // 2, 1)
        self.enemy_pos = Node(2 * self.board_size - 2, (2 * self.board_size - 1) // 2, 2)
        self.game.path_finding = PathFinding(self.board_size)
        self.game.update_board(self.board)
        self.game.n = self.board_size
        self.game.m = self.number_of_walls
        self.game.player_pos = self.player_pos
        self.game.enemy_pos = self.enemy_pos
        self.player_goal_row = 2 * self.board_size - 2
        self.enemy_goal_row = 0

        self.game.player_goal = self.player_goal_row
        self.game.enemy_goal = self.enemy_goal_row

        while True:
            try:
                print(f"{self.pending}Enter the number of walls that can be placed: ", end="")
                self.number_of_walls = int(input())
                break
            except ValueError:
                print(f"{self.pending}Please enter a valid number")

        self.player_walls = self.number_of_walls
        self.enemy_walls = self.number_of_walls

        while True:
            print(f"{self.pending}Do you want to start Y(es)/N(o)): ", end="")
            start = input().strip().upper()

            if start in ["Y", "YES", "VALHALLA"]:
                break
            elif start in ["N", "NO", "PESSI"]:
                label, move = self.game.min_max(self.board, True, self.player_pos, self.enemy_pos,
                                                self.player_walls, self.enemy_walls, max_depth=3)

                self.move(move, self.player_pos, 1)
                self.player_pos = Node(move.x, move.y, 1)

                break
            else:
                print(f"{self.pending}Please enter Y/Yes or N/No")

    def draw_game_stats(self):
        player_stats = f"{self.pending}P={self.player_name:<15} Walls left={self.player_walls * '|'}"
        bot_stats = f"{self.pending}B=BOT{'':<12} Walls left={self.enemy_walls * '|'}"

        print(player_stats)
        print(bot_stats)

    def render_winner(self, winner):
        if winner == 1:
            text = self.ENEMY_WINS
        elif winner == -1:
            text = self.PLAYER_WINS
        else:
            text = "\n"

        parts = text.split("\n")

        for p in parts:
            print(self.center_text(p))

        print()

    def draw_board(self):
        board_width = 4 * self.board_size - 1
        padding = " " * ((self.terminal_width - board_width) // 2 - 1)

        print(padding + " ", end="")
        for i in range(1, self.board_size + 1):
            print(f" {i}  ", end="")
        print()

        print(f"{padding}+{'-' * (4 * self.board_size - 1)}+")

        for i in range(2 * self.board_size - 1):
            print(f"{" " * ((self.terminal_width - board_width) // 2 - 4)}", end="")
            if i % 2 == 0:
                print(f"{i // 2 + 1:<2} |", end="")
            else:
                print(f"   |", end="")
            for j in range(2 * self.board_size - 1):
                if i % 2 == 0 and j % 2 == 0:
                    if self.board[i][j] == 1:
                        print(" B ", end="")
                    elif self.board[i][j] == 2:
                        print(" P ", end="")
                    else:
                        print(" * ", end="")
                else:
                    if i % 2 == 1 and j % 2 == 0:
                        print(" ", end="")
                    if self.board[i][j] == 9:
                        print("x", end="")
                    else:
                        print(" ", end="")
                    if i % 2 == 1 and j % 2 == 0:
                        print(" ", end="")
            if i % 2 == 1:
                print(f"| {chr(ord('A') + i // 2)} ")
            else:
                print("|")

        print(f"{padding}+{'-' * (4 * self.board_size - 1)}+")
        print(padding + "   ", end="")
        for i in range(self.board_size - 1):
            print(f" {chr(ord('a') + i)}  ", end="")
        print()

    def render(self):
        self.clear_screen()
        self.draw_game_stats()
        print()
        self.draw_board()

    def run(self):
        # self.display_logo()
        self.get_player_input()
        self.player_name = "Player"

        is_running = True
        message = self.YOUR_TURN
        winner = 0

        while is_running:
            ok = False
            self.render()
            print()
            print(self.pending, end="")
            print(message)
            print(self.pending, end="")
            user_input = input("Your move: ").strip()
            parts = user_input.split()

            message = self.ENEMY_TURN
            self.render()
            print()
            print(self.pending, end="")
            print(message)

            if not parts:
                print(self.center_text("Input cannot be empty."))
                continue
            parts[0] = parts[0].lower()

            if parts[0] == "l" and len(parts) == 3:
                try:
                    x = (int(parts[1]) - 1) * 2
                    y = (int(parts[2]) - 1) * 2
                    print(f"{self.pending}You moved to ({x}, {y})")
                    move = Move("L", y, x, None, None)

                    if self.game.check_if_valid_move(self.board.copy(), move, self.enemy_pos, 2, self.enemy_walls):
                        self.move(move, self.enemy_pos, 2)
                        self.enemy_pos = Node(move.x, move.y, 2)
                        self.render()

                        winner = self.game.is_game_over(self.board.copy())
                        ok = True

                        if winner != 0:
                            is_running = False
                            ok = False
                            break
                    else:
                        message = "Invalid move. Try again."

                except ValueError:
                    message = "Invalid move format. Use L x y where x and y are numbers."
            elif parts[0] == "w" and len(parts) == 3:
                l1 = parts[1]
                l2 = parts[2]
                if (l1.isupper() and l2.isupper()) or (l1.islower() and l2.islower()):
                    message = "Invalid wall format. Use W A B where A and B are letters."
                elif self.enemy_walls <= 0:
                    message = "You don't have any walls left."
                else:
                    move = None
                    if l1.isupper() and ord('A') <= ord(l1) <= ord('A') + self.board_size - 1 and ord('a') <= ord(
                            l2) <= ord('a') + self.board_size - 1:
                        x_mid = (ord(l1) - ord('A')) * 2 + 1
                        y_mid = (ord(l2) - ord('a')) * 2 + 1
                        move = Move("W", x_mid, y_mid - 1, x_mid, y_mid + 1)
                    elif l2.isupper() and ord('A') <= ord(l2) <= ord('A') + self.board_size - 1 and ord('a') <= ord(
                            l1) <= ord('a') + self.board_size - 1:
                        x_mid = (ord(l2) - ord('A')) * 2 + 1
                        y_mid = (ord(l1) - ord('a')) * 2 + 1
                        move = Move("W", x_mid - 1, y_mid, x_mid + 1, y_mid)
                    else:
                        message = "Invalid wall format. Use W A B where A and B are letters."

                    if move is not None:
                        self.game.path_finding.update_board(self.board.copy())
                        self.game.player_pos = self.player_pos
                        self.game.enemy_pos = self.enemy_pos
                        if self.game.check_if_valid_move(self.board.copy(), move, self.enemy_pos, 2, self.enemy_walls):
                            self.move(move, self.enemy_pos, 2)
                            self.enemy_walls -= 1
                            self.game.path_finding.board[move.x][move.y] = Node(move.x, move.y, 9)
                            self.game.path_finding.board[move.wx][move.wy] = Node(move.wx, move.wy, 9)
                            self.game.path_finding.board[(move.x + move.wx) // 2][(move.y + move.wy) // 2] = Node(
                                (move.x + move.wx) // 2, (move.y + move.wy) // 2, 9)
                            self.render()
                            ok = True


            elif parts[0] in ["exit", "quit", "q"]:
                self.render()
                print("\n")
                print(f"{self.pending}Exiting the game. Goodbye!")
                time.sleep(1.5)
                is_running = False
            else:
                message = "Invalid command. Please try again."

            if ok:
                self.game.player_pos = self.player_pos
                self.game.enemy_pos = self.enemy_pos
                self.game.player_goal = self.player_goal_row
                self.game.enemy_goal = self.enemy_goal_row

                label, move = self.game.min_max(self.board.copy(), True, self.player_pos, self.enemy_pos,
                                                self.player_walls, self.enemy_walls, max_depth=3)
                print(self.player_pos)
                self.move(move, self.player_pos, 1)
                if move.move == "L":
                    self.player_pos = Node(move.x, move.y, 1)

                # print(self.player_pos)
                # print(self.enemy_pos)
                # print(move)
                # print(self.board)

                # time.sleep(10)
                winner = self.game.is_game_over(self.board.copy())

                if winner != 0:
                    is_running = False
                else:
                    self.render()

        self.render()
        self.render_winner(winner)


def main():
    game = QuoridorUI()
    game.run()


if __name__ == "__main__":
    main()

import os
import time
from L04_bnam0365 import Quoridor

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

    def __init__(self):
        self.game = Quoridor()
        self.terminal_width = self.get_terminal_width()
        self.terminal_height = self.get_terminal_height()
        self.board_size = 3
        self.player_name = "Player"
        self.game_board = [
                [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            ]

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
        for line in self.LOGO.split('\n'):
            print(self.center_text(line))
        time.sleep(2)  # Show logo for 1 second

    def get_player_input(self):
        self.clear_screen()
        print(self.center_text("Welcome to Quoridor!"))
        print()

        # Get player name
        print(" " * (self.terminal_width // 4), end="")
        print("Enter your name: ", end="")
        self.player_name = input().strip()
        while not self.player_name:
            print(" " * (self.terminal_width // 4), end="")
            print("Name cannot be empty!")
            print(" " * (self.terminal_width // 4), end="")
            print("Enter your name: ",end="")
            self.player_name = input().strip()
        # Get board size
        while True:
            try:
                print(" " * (self.terminal_width // 4), end="")
                print("Enter the board size (3-10): ", end="")
                self.board_size = int(input())
                if 3 <= self.board_size <= 10:
                    break
                print(self.center_text("Please enter a number between 3 and 10"))
            except ValueError:
                print(self.center_text("Please enter a valid number"))

    def draw_game_stats(self):
        player_stats = f"P={self.player_name:<15} Walls left={self.game.player_walls * '|'}"
        bot_stats = f"B=BOT{'':<12} Walls left={self.game.enemy_walls * '|'}"

        print(self.center_text(player_stats))
        print(self.center_text(bot_stats))

    def draw_board(self):
        board_width = 4 * self.board_size - 1
        padding = " " * ((self.terminal_width - board_width) // 2 - 1)

        print(padding + " ", end="")
        for i in range(1, self.board_size + 1):
            print(f" {i}  ",end="")
        print()

        print(f"{padding}+{'-' * (4 * self.board_size - 1)}+")

        for i in range(2 * self.board_size - 1):
            print(f"{" " * ((self.terminal_width - board_width) // 2 - 4)}", end="")
            if i % 2 == 0:
                print(f"{i // 2 + 1:<2} |",end="")
            else:
                print(f"   |", end="")
            for j in range(2 * self.board_size - 1):
                if i % 2 == 0 and j % 2 == 0:
                    if self.game_board[i][j] == 1:
                        print(" P ", end="")
                    elif self.game_board[i][j] == 2:
                        print(" B ", end="")
                    else:
                        print(" * ", end="")
                else:
                    if i % 2 == 1 and j % 2 == 0:
                        print(" ", end="")
                    if self.game_board[i][j] == 9:
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
        self.display_logo()
        self.get_player_input()
        self.game.player_walls = 5
        self.game.enemy_walls = 4
        is_running = True

        while is_running:
            self.render()
            break


def main():
    game = QuoridorUI()
    game.run()

if __name__ == "__main__":
    main()
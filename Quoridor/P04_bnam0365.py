import os

from Quoridor.L04_bnam0365 import Quoridor

logo = r"""
 ________  ___  ___  ________  ________  ___  ________  ________  ________     
|\   __  \|\  \|\  \|\   __  \|\   __  \|\  \|\   ___ \|\   __  \|\   __  \    
\ \  \|\  \ \  \\\  \ \  \|\  \ \  \|\  \ \  \ \  \_|\ \ \  \|\  \ \  \|\  \   
 \ \  \\\  \ \  \\\  \ \  \\\  \ \   _  _\ \  \ \  \ \\ \ \  \\\  \ \   _  _\  
  \ \  \\\  \ \  \\\  \ \  \\\  \ \  \\  \\ \  \ \  \_\\ \ \  \\\  \ \  \\  \| 
   \ \_____  \ \_______\ \_______\ \__\\ _\\ \__\ \_______\ \_______\ \__\\ _\ 
    \|___| \__\|_______|\|_______|\|__|\|__|\|__|\|_______|\|_______|\|__|\|__|
          \|__|                                                                                            
"""

class QuoridorConsoleGame:
    def __init__(self):
        self.quoridor = Quoridor()
        self.n = 0
        self.name = None

    def start_game(self):
        print(logo)
        self.name = input("                                Enter your name:\n                                ")


def print_centered(text):
    # Get terminal size
    terminal_width = os.get_terminal_size().columns

    # Print each line centered
    for line in text.splitlines():
        print(line.center(terminal_width))

def main():
    quoridor = QuoridorConsoleGame()
    quoridor.start_game()
    os.system('clear' if os.name == 'posix' else 'cls')
    print_centered(logo)
    print_centered("Enter your name:")

    # Calculate the center position for input
    terminal_width = os.get_terminal_size().columns
    input_position = (terminal_width // 2) - 5

    # Print spaces to position the cursor at the center
    print(" " * input_position, end="")
    name = input()

    os.system('clear' if os.name == 'posix' else 'cls')
    print_centered(logo)
    print_centered(f"Welcome, {name}!")

if __name__ == "__main__":
    main()
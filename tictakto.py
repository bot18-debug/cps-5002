class TicTacToe:
    def __init__(self):
        # Initialise the game board with empty spaces
        self.__board = [' ' for _ in range(9)]

    def __display_board(self):
        """Display the current state of the board."""
        print()
        for row in range(3):
            print(" | ".join(self.__board[row * 3:(row + 1) * 3]))
            if row < 2:
                print("---------")
        print()

    def __player_move(self):
        """Handle the player's move."""
        position = int(input("Enter your move (0–8): "))
        # While the position is invalid, ask the user to enter it again
        while position < 0 or position > 8 or self.__board[position] != ' ':
            position = int(input("Invalid move. Try again (0–8): "))
        self.__board[position] = 'X'

    def run(self):
        """Main game loop."""
        print("Welcome to Tic-Tac-Toe.\nYou are player X. I am player O.\n")
        while True:
            self.__display_board()
            self.__player_move()


# Example usage:
if __name__ == "__main__":
    # Instantiate and start the game
    game = TicTacToe()
    game.run()


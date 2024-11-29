from newGame import generate_game_alternative

class GameState:
    def __init__(self, size):
        """
        Initialize the game state with a given board size.
        """
        self.size = size
        self.board = [["Undefined" for _ in range(size)] for _ in range(size)]
        self.solution = [["Undefined" for _ in range(size)] for _ in range(size)]
        self.row_conditions = [[0] for _ in range(size)]  # Initial row requirements set to [0]
        self.col_conditions = [[0] for _ in range(size)]  # Initial column requirements set to [0]

    def generate_new_game(self):
        """
        Generate a new game using the alternative method.
        """
        self.reset_board()
        self.solution, self.row_conditions, self.col_conditions = generate_game_alternative(self.size)

    def reset_board(self):
        """
        Reset the board to its initial state.
        """
        self.board = [["Undefined" for _ in range(self.size)] for _ in range(self.size)]

    def update_cell(self, x, y):
        """
        Update the value of a specific cell and cycle through its states.
        """
        current_value = self.board[x][y]
        if current_value == "Undefined":
            self.board[x][y] = True
        elif current_value is True:
            self.board[x][y] = False
        elif current_value is False:
            self.board[x][y] = "Undefined"
        return self.board[x][y]

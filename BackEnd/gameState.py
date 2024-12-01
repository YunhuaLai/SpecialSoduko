from newGame import generate_game_alternative
import humanSolution as hs

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

    def update_cell(self, x, y , value = None):
        """
        Update the value of a specific cell and cycle through its states.
        """
        if value is not None:
            self.board[x][y] = value
            return self.board[x][y]
        
        current_value = self.board[x][y]
        if current_value == "Undefined":
            self.board[x][y] = True
        elif current_value is True:
            self.board[x][y] = False
        elif current_value is False:
            self.board[x][y] = "Undefined"
        return self.board[x][y]
    
    def evaluate_complexity(self):
        """
        Evaluate the complexity of solving the board.

        Args:
        - board: Current state of the board (2D list of True, False, or "Undefined").
        - row_requirements: List of row requirements.
        - col_requirements: List of column requirements.

        Returns:
        - Total complexity mark.
        """
        size = self.size
        row_requirements = self.row_conditions
        col_requirements = self.col_conditions
        board = self.board
        total_complexity = 0

        while True:
            solvable_cells = []

            # Step 1: Identify solvable cells
            for i in range(size):
                # Generate possibilities for the row
                row_possibilities = hs.generate_possibilities(size, row_requirements[i], board[i])
                if len(row_possibilities) > 1:
                    common_row = hs.find_common_solution(row_possibilities)
                    for j in range(size):
                        if board[i][j] == "Undefined" and common_row[j] != "Undefined":
                            solvable_cells.append({
                                "x": i,
                                "y": j,
                                "type": "row",
                                "complexity": len(row_possibilities),
                            })
                # Generate possibilities for the column
                column = [board[x][i] for x in range(size)]
                col_possibilities =hs.generate_possibilities(size, col_requirements[i], column)
                if len(col_possibilities) > 1:
                    common_col = hs.find_common_solution(col_possibilities)
                    for j in range(size):
                        if board[j][i] == "Undefined" and common_col[j] != "Undefined":
                            solvable_cells.append({
                                "x": j,
                                "y": i,
                                "type": "column",
                                "complexity": len(col_possibilities),
                            })

            # Step 2: Check if no cells are solvable
            if not solvable_cells:
                break  # No more cells can be solved

            # Step 3: Classify solvable cells by complexity
            solvable_cells.sort(key=lambda cell: cell["complexity"])  # Sort by complexity
            easiest_cells = [cell for cell in solvable_cells if cell["complexity"] == solvable_cells[0]["complexity"]]

            # Step 4: Fill the easiest cells and accumulate complexity mark
            for cell in easiest_cells:
                x, y = cell["x"], cell["y"]
                if cell["type"] == "row":
                    row_possibilities = hs.generate_possibilities(size, row_requirements[x], board[x])
                    common_row = hs.find_common_solution(row_possibilities)
                    board[x][y] = common_row[y]
                elif cell["type"] == "column":
                    column = [board[i][y] for i in range(size)]
                    col_possibilities = hs.generate_possibilities(size, col_requirements[y], column)
                    common_col = hs.find_common_solution(col_possibilities)
                    board[x][y] = common_col[x]

                # Add complexity mark
                total_complexity += 2 ** cell["complexity"]

        return total_complexity
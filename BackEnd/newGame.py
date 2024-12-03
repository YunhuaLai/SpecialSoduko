import random
import humanSolution as hs
import gameState

def derive_requirements(board):
    """
    Derive row and column requirements based on a given 2D board.

    Args:
    - board: A 2D list of True, False, and "Undefined" values.

    Returns:
    - row_requirements: List of requirements for rows.
    - col_requirements: List of requirements for columns.
    """
    def extract_segments(line):
        segments = []
        count = 0
        for cell in line:
            if cell == True:
                count += 1
            elif count > 0:
                segments.append(count)
                count = 0
        if count > 0:
            segments.append(count)
        return segments if segments else [0]  # Return [0] if no segments are found

    row_requirements = [extract_segments(row) for row in board]
    col_requirements = [
        extract_segments([board[i][j] for i in range(len(board))])
        for j in range(len(board[0]))
    ]

    return row_requirements, col_requirements


def generate_random_board(size):
    """
    Generate a random 2D board with True, False, and "Undefined" values.

    Args:
    - size: The size of the board (size x size).

    Returns:
    - A 2D board.
    """
    return [[random.choice([True, False]) for _ in range(size)] for _ in range(size)]


def generate_game_alternative(size):
    """
    Generate a game by creating a random board, deriving requirements, and checking uniqueness.

    Args:
    - size: The size of the board (e.g., 10 for a 10x10 board).

    Returns:
    - A tuple (board, row_requirements, col_requirements) if unique; otherwise, retries.
    """
    while True:
        # Generate a random board
        random_board = generate_random_board(size)

        game_state = gameState.GameState(size)

        # Derive row and column requirements
        row_requirements, col_requirements = derive_requirements(random_board)
        game_state.row_conditions = row_requirements
        game_state.col_conditions = col_requirements

        # Solve the board
        solved_board = hs.solve_with_common_logic(game_state)

        # Check if the solved board matches the original random board
        if solved_board == random_board:
            return solved_board, row_requirements, col_requirements
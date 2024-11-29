import humanSolution as hs


def evaluate_complexity(board, row_requirements, col_requirements):
    """
    Evaluate the complexity of solving the board.

    Args:
    - board: Current state of the board (2D list of True, False, or "Undefined").
    - row_requirements: List of row requirements.
    - col_requirements: List of column requirements.

    Returns:
    - Total complexity mark.
    """
    size = len(board)
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


if __name__ == "__main__":
    # Example board and requirements
    board = [
        ["Undefined", "Undefined", True, "Undefined"],
        ["Undefined", True, "Undefined", "Undefined"],
        [True, "Undefined", "Undefined", "Undefined"],
        ["Undefined", "Undefined", "Undefined", "Undefined"]
    ]

    row_requirements = [[1], [1, 1], [1], [1]]
    col_requirements = [[1], [1, 1], [1], [1]]

    complexity = evaluate_complexity(board, row_requirements, col_requirements)
    print("Total Complexity:", complexity)

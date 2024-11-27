def generate_possibilities(size, requirement, current_line):
    """
    Generate all valid possibilities for a row/column given its size, requirement, and current state.
    """
    def helper(remaining_req, remaining_space):
        if not remaining_req:  # No more segments to place
            return [[False] * remaining_space]

        first_segment = [True] * remaining_req[0]
        results = []

        for start in range(remaining_space - len(first_segment) + 1):
            # Place the current segment
            current = [False] * start + first_segment
            # Add at least one False after this segment (if more segments remain)
            if len(remaining_req) > 1:
                current += [False]
            # Recurse for the remaining segments
            remaining_results = helper(remaining_req[1:], remaining_space - len(current))
            for result in remaining_results:
                results.append(current + result)

        return results

    # Start the recursive generation
    all_possibilities = helper(requirement, size)

    # Filter out solutions that conflict with the current line
    valid_possibilities = []
    for possibility in all_possibilities:
        conflict = False
        for i in range(size):
            if current_line[i] != "Undefined" and current_line[i] != possibility[i]:
                conflict = True
                break
        if not conflict:
            valid_possibilities.append(possibility)

    return valid_possibilities



def find_common_solution(possibilities):
    """
    Find the common cells (True or False) in all possibilities.
    """
    common = possibilities[0][:]  # Start with the first possibility
    for possibility in possibilities[1:]:
        for i in range(len(common)):
            if common[i] != possibility[i]:
                common[i] = "Undefined"
    return common


def solve_with_common_logic(size, row_requirements, col_requirements):
    """
    Solve the puzzle using the logic of unique solutions and common cells.
    """
    board = [["Undefined" for _ in range(size)] for _ in range(size)]
    changes = True

    while changes:
        changes = False

        # Process rows
        for i, requirement in enumerate(row_requirements):
            if all(cell != "Undefined" for cell in board[i]):
                continue  # Skip fully filled rows
            
            possibilities = generate_possibilities(size, requirement, board[i])
            if len(possibilities) == 1:  # Unique solution
                board[i] = possibilities[0]
                changes = True
            else:  # Find common cells
                common_solution = find_common_solution(possibilities)
                for j in range(size):
                    if board[i][j] == "Undefined" and common_solution[j] != "Undefined":
                        board[i][j] = common_solution[j]
                        changes = True

        # Process columns
        for j, requirement in enumerate(col_requirements):
            column = [board[i][j] for i in range(size)]
            if all(cell != "Undefined" for cell in column):
                continue  # Skip fully filled columns
            
            possibilities = generate_possibilities(size, requirement, column)
            if len(possibilities) == 1:  # Unique solution
                for i in range(size):
                    board[i][j] = possibilities[0][i]
                changes = True
            else:  # Find common cells
                common_solution = find_common_solution(possibilities)
                for i in range(size):
                    if board[i][j] == "Undefined" and common_solution[i] != "Undefined":
                        board[i][j] = common_solution[i]
                        changes = True

    return board


if __name__ == '__main__':
    size = 10
    row_conditions = [
        [2, 2], [4, 4], [3, 4], [2, 2, 2, 1], [2, 4], [9], [10], [10], [9], [2, 2]
    ]
    col_conditions = [
        [3, 2], [4, 4], [3, 6], [1 ,7], [1, 4], [2, 5], [9], [10], [2, 6], [1, 4]
    ]

    solution = solve_with_common_logic(size, row_conditions, col_conditions)
    for row in solution:
        print(row)


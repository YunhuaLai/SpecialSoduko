# utils.py

def extract_true_segments(line):
    """Extract lengths of successive True segments in a row/column."""
    segments = []
    count = 0
    for cell in line:
        if cell == True:
            count += 1
        elif cell != True and count > 0:
            segments.append(count)
            count = 0
    if count > 0:  # Append the last segment if it ends with True
        segments.append(count)
    return segments

def check_conditions(board, row_conditions, col_conditions):
    """Validate that the board satisfies all row and column conditions."""
    size = len(board)

    # Check rows
    for i, row in enumerate(board):
        actual_segments = extract_true_segments(row)
        expected_segments = row_conditions[i]
        if actual_segments != expected_segments:
            return False, f"Row {i} does not satisfy the condition: {actual_segments} != {expected_segments}"

    # Check columns
    for j in range(size):
        column = [board[i][j] for i in range(size)]  # Extract the column
        actual_segments = extract_true_segments(column)
        expected_segments = col_conditions[j]
        if actual_segments != expected_segments:
            return False, f"Column {j} does not satisfy the condition: {actual_segments} != {expected_segments}"

    return True, "All conditions are satisfied!"

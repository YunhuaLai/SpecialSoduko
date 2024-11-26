# settings.py

size = 10

# Initialize the chessboard state
board = [["Undefined" for _ in range(size)] for _ in range(size)]

# Row and column conditions
row_conditions = [
    [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [0, 9]
]
col_conditions = [
    [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [0, 9]
]

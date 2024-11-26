# settings.py

size = 10

# Initialize the chessboard state
board = [["Undefined" for _ in range(size)] for _ in range(size)]

# Row and column conditions
row_conditions = [
    [2, 2], [4, 4], [3, 4], [2, 2, 2, 1], [2, 4], [9], [10], [10], [9], [2, 2]
]
col_conditions = [
    [3, 2], [4, 4], [3, 6], [1 ,7], [1, 4], [2, 5], [9], [10], [2, 6], [1, 4]
]

from flask import Flask, jsonify, request, send_from_directory
from settings import size, board, row_conditions, col_conditions
from utils import validate_line
import os

app = Flask(__name__, static_folder="../FrontEnd", static_url_path="/static")

@app.route('/get_board', methods=['GET'])
def get_board():
    return jsonify({
        "board": board,
        "row_conditions": row_conditions,
        "col_conditions": col_conditions
    })

@app.route('/update_cell', methods=['POST'])
def update_cell():
    data = request.json
    x, y = data['x'], data['y']
    current_value = board[x][y]

    # Cycle the value: Undefined → True → False → Undefined
    if current_value == "Undefined":
        board[x][y] = True
    elif current_value == True:
        board[x][y] = False
    elif current_value == False:
        board[x][y] = "Undefined"

    # Validate row and column
    row_violations = validate_line(board[x], row_conditions[x])
    column_violations = validate_line([board[i][y] for i in range(size)], col_conditions[y])
    print(row_violations, column_violations)
    return jsonify({
        "message": "Cell updated",
        "new_value": board[x][y],
        "row_violations": row_violations,
        "column_violations": column_violations
    })

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)

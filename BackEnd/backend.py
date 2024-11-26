from flask import Flask, jsonify, request, send_from_directory
import os

# Flask app initialization
app = Flask(__name__, static_folder="../FrontEnd", static_url_path="/static")

# Initialize the chessboard state
size = 10
board = [["Undefined" for _ in range(size)] for _ in range(size)]

# Row and column conditions
row_conditions = [
    [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [0, 9]
]
col_conditions = [
    [0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 7], [7, 8], [8, 9], [0, 9]
]

@app.route('/get_board', methods=['GET'])
def get_board():
    # Return the board state and conditions
    return jsonify({
        "board": board,
        "row_conditions": row_conditions,
        "col_conditions": col_conditions
    })

@app.route('/update_cell', methods=['POST'])
def update_cell():
    # Update a specific cell in the chessboard
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

    return jsonify({"message": "Cell updated", "new_value": board[x][y]})

@app.route('/')
def serve_index():
    # Serve the index.html file
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    # Serve other static files like JavaScript and CSS
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)

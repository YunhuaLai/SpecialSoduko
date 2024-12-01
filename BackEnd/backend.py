from flask import Flask, jsonify, request, send_from_directory
from settings import size  # Import initial size
from utils import validate_line
import humanSolution as hs
from newGame import generate_game_alternative
from gameState import GameState
import complexity as cp
import os

# Initialize Flask app
app = Flask(__name__, static_folder="../FrontEnd", static_url_path="/static")

# Initialize game state
game_state = GameState(size)

@app.route('/get_board', methods=['GET'])
def get_board():
    """
    Retrieve the current board and conditions.
    """
    return jsonify({
        "board": game_state.board,
        "row_conditions": game_state.row_conditions,
        "col_conditions": game_state.col_conditions
    })

@app.route('/update_cell', methods=['POST'])
def update_cell():
    """
    Update a specific cell and validate the corresponding row and column.
    """
    data = request.json
    x, y = data['x'], data['y']
    new_value = game_state.update_cell(x, y)

    # Validate row and column
    row_violations = validate_line(game_state.board[x], game_state.row_conditions[x])
    column_violations = validate_line(
        [game_state.board[i][y] for i in range(game_state.size)],
        game_state.col_conditions[y]
    )
    return jsonify({
        "message": "Cell updated",
        "new_value": new_value,
        "row_violations": row_violations,
        "column_violations": column_violations
    })

@app.route('/')
def serve_index():
    """
    Serve the index.html file.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """
    Serve static files like JavaScript and CSS.
    """
    return send_from_directory(app.static_folder, path)

@app.route('/solve_game', methods=['POST'])
def solve_game():
    """
    Solve the puzzle and return the solved board.
    """
    solved_board = hs.solve_with_common_logic(game_state)
    return jsonify({"solved_board": solved_board})

@app.route('/get_hint', methods=['POST'])
def get_hint():
    """
    Provide the next logical move as a hint.
    """
    hint = hs.get_hint_logic(game_state)

    # Check if a valid hint is returned
    if "error" in hint:
        return jsonify({"error": hint["error"]})

    # Update the board with the hint
    game_state.update_cell(hint["x"], hint["y"], hint["value"])
    return jsonify(hint)

@app.route('/check_board', methods=['POST'])
def check_board():
    """
    Check the current board state for incorrect cells.
    """
    incorrect_cells = hs.check_board_logic(game_state)
    return jsonify({"incorrect_cells": incorrect_cells})

@app.route('/reset_board', methods=['POST'])
def reset_board():
    """
    Reset the board to its initial state.
    """
    game_state.reset_board()
    return jsonify({"message": "Board reset successfully", "board": game_state.board})

@app.route('/generate_game_alternative', methods=['GET'])
def generate_game_alternative_endpoint():
    """
    Generate a new game using the alternative method.
    """
    game_state.generate_new_game()
    return jsonify({
        "board": game_state.board,
        "row_conditions": game_state.row_conditions,
        "col_conditions": game_state.col_conditions
    })

@app.route('/complexity', methods=['POST'])
def evaluate_complexity():
    """
    Evaluate the complexity of a given board.
    """
    complexity = cp.evaluate_complexity(game_state)
    
    return jsonify({"complexity": complexity})

if __name__ == '__main__':
    app.run(debug=True)

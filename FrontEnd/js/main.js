// main.js

window.onload = async () => {
    await loadBoard();
};

document.getElementById("solveButton").addEventListener("click", async () => {
    // Send a request to solve the game
    const response = await fetch(`${API_BASE_URL}/solve_game`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();
    const solvedBoard = data.solved_board;

    // Update the board with the solved state
    updateBoard(solvedBoard);
});

function updateBoard(solvedBoard) {
    const table = document.getElementById("chessboard");

    // Update each cell based on the solved board
    solvedBoard.forEach((row, i) => {
        row.forEach((cell, j) => {
            const cellElement = table.rows[i + 1]?.cells[j + 1]; // Skip the header row and column
            if (cellElement) {
                cellElement.className =
                    cell === true ? "true" : cell === false ? "false" : "undefined";
            }
        });
    });
}


document.getElementById("hintButton").addEventListener("click", async () => {
    // Get the current board state
    console.log("Hint button clicked");
    const table = document.getElementById("chessboard");
    const currentBoard = [];
    for (let i = 1; i < table.rows.length; i++) { // Skip header row
        const row = [];
        for (let j = 1; j < table.rows[i].cells.length; j++) { // Skip header column
            const cell = table.rows[i].cells[j];
            if (cell.classList.contains("true")) {
                row.push(true);
            } else if (cell.classList.contains("false")) {
                row.push(false);
            } else {
                row.push("Undefined");
            }
        }
        currentBoard.push(row);
    }

    // Send the board state to the backend for a hint
    const response = await fetch(`${API_BASE_URL}/get_hint`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            board: currentBoard,
        }),
    });

    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }

    // Update the board with the hint
    const { x, y, value } = data;
    const cellElement = table.rows[x + 1]?.cells[y + 1]; // Skip header row/column
    if (cellElement) {
        cellElement.className = value === true ? "true" : value === false ? "false" : "undefined";
    }
});
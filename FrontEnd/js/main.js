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

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
    console.log("Hint button clicked");

    try {
        const response = await fetch(`${API_BASE_URL}/get_hint`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        // Update the board with the hint
        const { x, y, value } = data;
        const table = document.getElementById("chessboard"); // Ensure table is defined
        const cellElement = table.rows[x + 1]?.cells[y + 1]; // Skip header row/column
        if (cellElement) {
            cellElement.className = value === true ? "true" : value === false ? "false" : "undefined";
        }
    } catch (error) {
        console.error("Failed to get a hint:", error);
        alert("Failed to get a hint. Please try again.");
    }
});

document.getElementById("resetButton").addEventListener("click", async () => {
    const response = await fetch(`${API_BASE_URL}/reset_board`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    });

    const data = await response.json();
    console.log(data.message); // Log the reset message

    const newBoard = data.board;
    const table = document.getElementById("chessboard");

    // Reset the board in the UI
    newBoard.forEach((row, i) => {
        row.forEach((cell, j) => {
            const cellElement = table.rows[i + 1]?.cells[j + 1]; // Skip header row/column
            if (cellElement) {
                cellElement.className = "undefined"; // Reset all cells to undefined
            }
        });
    });

    alert("The board has been reset!");
});



document.getElementById("checkButton").addEventListener("click", async () => {
    console.log("Check button clicked");
    const table = document.getElementById("chessboard"); // Ensure table reference

    try {
        const response = await fetch(`${API_BASE_URL}/check_board`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        const incorrectCells = data.incorrect_cells;

        // Clear previous incorrect highlights
        for (let i = 1; i < table.rows.length; i++) {
            for (let j = 1; j < table.rows[i].cells.length; j++) {
                table.rows[i].cells[j].classList.remove("incorrect");
            }
        }

        // Highlight incorrect cells
        incorrectCells.forEach(({ x, y }) => {
            const cellElement = table.rows[x + 1]?.cells[y + 1]; // Skip header row/column
            if (cellElement) {
                cellElement.classList.add("incorrect");
            }
        });
    } catch (error) {
        console.error("Failed to check the board:", error);
        alert("Failed to check the board. Please try again.");
    }
});


document.getElementById("newGameButton").addEventListener("click", async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/generate_game_alternative`);
        if (!response.ok) {
            throw new Error(`Failed to fetch new game: ${response.statusText}`);
        }

        const data = await response.json();
        const { board, row_conditions, col_conditions } = data; // Match backend response keys

        // Update global game state
        window.gameState = {
            board,
            row_conditions,
            col_conditions
        };

        // Reload the board with new data
        loadBoard(true); // Pass true to clear the board
    } catch (error) {
        console.error("Error fetching new game:", error);
        alert("Failed to load a new game. Please try again.");
    }
});


document.getElementById("evalComplexityButton").addEventListener("click", async () => {
    // Ensure the board and conditions are fetched from the global state
    const board = window.gameState.board;
    const row_conditions = window.gameState.row_conditions;
    const col_conditions = window.gameState.col_conditions;

    try {
        const response = await fetch(`${API_BASE_URL}/complexity`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                board,
                row_conditions,
                col_conditions,
            }),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        const complexity = data.complexity;

        alert(`The complexity of the current board is: ${complexity}`);
    } catch (error) {
        console.error("Failed to evaluate complexity:", error);
        alert("Failed to evaluate the complexity. Please try again.");
    }
});


// board.js

const API_BASE_URL = 'http://127.0.0.1:5000';

async function loadBoard(empty = false) {
    const response = await fetch(`${API_BASE_URL}/get_board`);
    const data = await response.json();

    const table = document.getElementById('chessboard');
    table.innerHTML = ''; // Clear existing board

    // Add column conditions
    let headerRow = document.createElement('tr');
    headerRow.innerHTML = '<th></th>'; // Empty top-left corner for alignment
    data.col_conditions.forEach((col, index) => {
        let th = document.createElement('th');
        th.classList.add('col-condition'); // Add col-condition class
        th.setAttribute('data-index', index); // Add data-index for identification

        // Create individual spans for each segment of the column condition
        th.innerHTML = col.map(segment => `<span class="condition-segment">${segment}</span>`).join(', ');
        headerRow.appendChild(th); // Append to the header row
    });
    table.appendChild(headerRow);

    // Add rows with row conditions and cells
    data.board.forEach((row, i) => {
        let rowElement = document.createElement('tr');

        // Add row condition
        let rowHeader = document.createElement('th');
        rowHeader.classList.add('row-condition'); // Add row-condition class
        rowHeader.setAttribute('data-index', i); // Add data-index for identification

        // Create individual spans for each segment of the row condition
        rowHeader.innerHTML = data.row_conditions[i].map(segment => `<span class="condition-segment">${segment}</span>`).join(', ');
        rowElement.appendChild(rowHeader);

        // Add cells
        row.forEach((cell, j) => {
            let cellElement = document.createElement('td');
            if (!empty) {
                cellElement.className = cell === true ? 'true' : cell === false ? 'false' : 'undefined';
            } else {
                cellElement.className = 'undefined'; // Reset all cells to undefined if empty is true
            }
            cellElement.onclick = () => updateCell(i, j, cellElement);
            rowElement.appendChild(cellElement);
        });

        table.appendChild(rowElement); // Append the row to the table after all cells are added
    });
}

async function updateCell(x, y, cellElement) {
    const response = await fetch(`${API_BASE_URL}/update_cell`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x, y })
    });
    const data = await response.json();

    console.log("Backend response:", data); // Check row_violations and column_violations

    const newValue = data.new_value;
    cellElement.className = newValue === true ? 'true' : newValue === false ? 'false' : 'undefined';

    // Highlight row and column violations
    highlightViolations(x, 'row', data.row_violations);
    highlightViolations(y, 'col', data.column_violations);
}

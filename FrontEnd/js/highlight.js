// highlight.js

function highlightViolations(index, type, violations) {
    // Select the main condition element (the <th>)
    const conditionElement = document.querySelector(
        `.${type}-condition[data-index="${index}"]`
    );
    if (!conditionElement) {
        console.error(`No ${type}-condition element found for index ${index}`);
        return;
    }

    // Select individual condition segments (<span>)
    const segments = conditionElement.querySelectorAll('.condition-segment');

    // Apply or remove the violation class for each segment
    segments.forEach((el, i) => {
        if (i < violations.length && violations[i]) {
            el.classList.add('violation'); // Highlight the segment with a violation
        } else {
            el.classList.remove('violation'); // Remove highlight if no violation
        }
    });
}

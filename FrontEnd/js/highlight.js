// highlight.js

function highlightViolations(index, type, violations) {
    console.log(`Highlighting violations for ${type} at index ${index}:`, violations);

    // Select the main condition element (the <th>)
    const conditionElement = document.querySelector(
        `.${type}-condition[data-index="${index}"]`
    );
    console.log(`Condition element for ${type} at index ${index}:`, conditionElement);

    if (!conditionElement) {
        console.error(`No ${type}-condition element found for index ${index}`);
        return;
    }

    // Select individual condition segments (<span>)
    const segments = conditionElement.querySelectorAll('.condition-segment');
    console.log(`Segments found for ${type} index ${index}:`, segments);
    console.log(`Segments length: ${segments.length}, Violations length: ${violations.length}`);

    // Apply or remove the violation class for each segment
    segments.forEach((el, i) => {
        if (i < violations.length && violations[i]) {
            el.classList.add('violation'); // Highlight the segment with a violation
            console.log(`Violation added to ${type} segment ${i}:`, el);
        } else {
            el.classList.remove('violation'); // Remove highlight if no violation
            console.log(`Violation removed from ${type} segment ${i}:`, el);
        }
    });
}

//BET TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("bet-toggle");
    const section = document.getElementById("bet-section");

    toggle.addEventListener("change", () => {
        if (toggle.checked) {
            section.style.display = "block";
        } else {
            section.style.display = "none";
        }
    });

    // Initialize the visibility based on the toggle's initial state
    section.style.display = toggle.checked ? "block" : "none";
});
//GAME TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("game-toggle");
    const section = document.getElementById("general-section");
    const dice = document.getElementById("dice-block");
    const rps = document.getElementById("rps-block");
    const hball = document.getElementById("hball-block");
    const bet = document.getElementById("bet-block");

    toggle.addEventListener("change", () => {
        if (toggle.checked) {
            section.style.display = "block";
            dice.style.display = "block";
            rps.style.display = "block";
            hball.style.display = "block";
            bet.style.display = "block";
        } else {
            section.style.display = "none";
            dice.style.display = "none";
            rps.style.display = "none";
            hball.style.display = "none";
            bet.style.display = "none";
        }
    });

    // Initialize the visibility based on the toggle's initial state
    section.style.display = toggle.checked ? "block" : "none";
    dice.style.display = toggle.checked ? "block" : "none";
    rps.style.display = toggle.checked ? "block" : "none";
    hball.style.display = toggle.checked ? "block" : "none";
    bet.style.display = toggle.checked ? "block" : "none";
});

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
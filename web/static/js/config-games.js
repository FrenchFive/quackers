import { saveConfig } from "./utils.js";

//GAME TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("game-toggle");
    const section = document.getElementById("general-section");
    const dice = document.getElementById("dice-block");
    const rps = document.getElementById("rps-block");
    const hball = document.getElementById("hball-block");
    const bet = document.getElementById("bet-block");
    const roll = document.getElementById("roll-block");
    const quiz = document.getElementById("quiz-block");

    toggle.addEventListener("change", () => {
        if (toggle.checked) {
            section.style.display = "block";
            dice.style.display = "block";
            rps.style.display = "block";
            hball.style.display = "block";
            bet.style.display = "block";
            roll.style.display = "block";
            quiz.style.display = "block";
        } else {
            section.style.display = "none";
            dice.style.display = "none";
            rps.style.display = "none";
            hball.style.display = "none";
            bet.style.display = "none";
            roll.style.display = "none";
            quiz.style.display = "none";
        }
    });

    // Initialize the visibility based on the toggle's initial state
    section.style.display = toggle.checked ? "block" : "none";
    dice.style.display = toggle.checked ? "block" : "none";
    rps.style.display = toggle.checked ? "block" : "none";
    hball.style.display = toggle.checked ? "block" : "none";
    bet.style.display = toggle.checked ? "block" : "none";
    roll.style.display = toggle.checked ? "block" : "none";
    quiz.style.display = toggle.checked ? "block" : "none";
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

//QUIZ TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("quiz-toggle");
    const section = document.getElementById("quiz-section");
    const inputField = document.getElementById("quiz-channel");

    toggle.addEventListener("change", () => {
        if (toggle.checked) {
            section.style.display = "block";
            inputField.disabled = false;
        } else {
            section.style.display = "none";
            inputField.disabled = true;
        }
    });

    section.style.display = toggle.checked ? "block" : "none";
    if (!toggle.checked) {
        inputField.disabled = true;
    }
});

//DISABLE INPUT Limitation of the amount Gambled 
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('game-limit-toggle');
    const inputField = document.getElementById('game-limit-input');

    toggle.addEventListener('change', () => {
        if (toggle.checked) {
            inputField.disabled = false;
        } else {
            inputField.disabled = true;
        }
    });

    // Initial check
    if (!toggle.checked) {
        inputField.disabled = true;
    }
});

//DISABLE INPUT Limitation of the amount Betted
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('bet-limit-toggle');
    const inputField = document.getElementById('bet-limit-input');

    toggle.addEventListener('change', () => {
        if (toggle.checked) {
            inputField.disabled = false;
        } else {
            inputField.disabled = true;
        }
    });

    // Initial check
    if (!toggle.checked) {
        inputField.disabled = true;
    }
});

//BUTTON SAVE GAME
document.getElementById("btn-gme-gme").addEventListener("click", () => {
    const data = [
        { name: "game", value: document.getElementById("game-toggle").checked ? 1 : 0 },
        { name: "game_limit", value: document.getElementById("game-limit-toggle").checked ? 1 : 0 },
        { name: "game_limit_value", value: document.getElementById("game-limit-input").value },
    ];
    saveConfig(
        "btn-gme-gme",
        data,
    );
});

//BUTTON SAVE DICES
document.getElementById("btn-gme-dices").addEventListener("click", () => {
    const data = [
        { name: "dices", value: document.getElementById("dices-toggle").checked ? 1 : 0 },
    ];
    saveConfig(
        "btn-gme-dices",
        data,
    );
});

//BUTTON SAVE RPS
document.getElementById("btn-gme-rps").addEventListener("click", () => {
    const data = [
        { name: "rps", value: document.getElementById("rps-toggle").checked ? 1 : 0 },
    ];
    saveConfig(
        "btn-gme-rps",
        data,
    );
});

//BUTTON SAVE HEIGHTBALL
document.getElementById("btn-gme-hball").addEventListener("click", () => {
    const data = [
        { name: "hball", value: document.getElementById("hball-toggle").checked ? 1 : 0 },
    ];
    saveConfig(
        "btn-gme-hball",
        data,
    );
});

//BUTTON SAVE BET
document.getElementById("btn-gme-bet").addEventListener("click", () => {
    const data = [
        { name: "bet", value: document.getElementById("bet-toggle").checked ? 1 : 0 },
        { name: "bet_limit", value: document.getElementById("bet-limit-toggle").checked ? 1 : 0 },
        { name: "bet_limit_value", value: document.getElementById("bet-limit-input").value },
    ];
    saveConfig(
        "btn-gme-bet",
        data,
    );
});

//BUTTON SAVE ROLL
document.getElementById("btn-gme-roll").addEventListener("click", () => {
    const data = [
        { name: "roll", value: document.getElementById("roll-toggle").checked ? 1 : 0 },
    ];
    saveConfig(
        "btn-gme-roll",
        data,
    );
});

//BUTTON SAVE QUIZ
document.getElementById("btn-gme-quiz").addEventListener("click", () => {
    const data = [
        { name: "quiz_enable", value: document.getElementById("quiz-toggle").checked ? 1 : 0 },
        { name: "quiz_ch_id", value: document.getElementById("quiz-channel").value },
    ];
    saveConfig(
        "btn-gme-quiz",
        data,
    );
});

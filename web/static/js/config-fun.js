import { saveConfig } from "./utils.js";

//SOUND TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("sound-toggle");
    const section = document.getElementById("sound-section");

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

//SOUND PAY TOGGLE
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('sound-pay');
    const inputField = document.getElementById('sound-pay-value');

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

//BUTTON SAVE COIFFEUR
document.getElementById("btn-coiffeur").addEventListener("click", () => {
    const data = [
        { name: "fun_coiffeur", value: document.getElementById("coiffeur-toggle").checked ? 1 : 0 },
    ];

    saveConfig(
        "btn-coiffeur",
        data,
    );
});

//BUTTON SAVE SOUND
document.getElementById("btn-sound").addEventListener("click", () => {
    const data = [
        { name: "sound", value: document.getElementById("sound-toggle").checked ? 1 : 0 },
        { name: "sound_pay", value: document.getElementById("sound-pay").checked ? 1 : 0 },
        { name: "sound_pay_value", value: document.getElementById("sound-pay-value").value},
    ];

    saveConfig(
        "btn-sound",
        data,
    );
});
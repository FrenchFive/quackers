//COIN TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("coin-toggle");
    const section = document.getElementById("coin-section");
    const bankblock = document.getElementById("bank-block");
    const sendblock = document.getElementById("send-block");
    const dailyblock = document.getElementById("daily-block");

    toggle.addEventListener("change", () => {
        if (toggle.checked) {
            section.style.display = "block";
            bankblock.style.display = "block";
            sendblock.style.display = "block";
            dailyblock.style.display = "block";
        } else {
            section.style.display = "none";
            bankblock.style.display = "none";
            sendblock.style.display = "none";
            dailyblock.style.display = "none";
        }
    });

    // Initialize the visibility based on the toggle's initial state
    section.style.display = toggle.checked ? "block" : "none";
    bankblock.style.display = toggle.checked ? "block" : "none";
    sendblock.style.display = toggle.checked ? "block" : "none";
    dailyblock.style.display = toggle.checked ? "block" : "none";
});

//WELCOME TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("bank-toggle");
    const section = document.getElementById("bank-section");

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
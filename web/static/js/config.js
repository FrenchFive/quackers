//WELCOME TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("welcome-toggle");
    const section = document.getElementById("welcome-section");

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

//GOODBYE TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("goodbye-toggle");
    const section = document.getElementById("goodbye-section");

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

//PRESENTATION
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("presentation-toggle");
    const section = document.getElementById("presentation-section");

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
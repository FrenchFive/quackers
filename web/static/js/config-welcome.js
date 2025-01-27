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

//DIRECT MESSAGES
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("dm-toggle");
    const section = document.getElementById("dm-section");

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

//DISABLE Custom Welcome Message
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('wlc-cstm-msg-toggle');
    const inputField = document.getElementById('wlc-cstm-msg-input');

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

//DISABLE Random Emote
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('bot-reaction-toggle');
    const inputField = document.getElementById('bot-random-reaction-toggle');

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

//DISABLE Custom Welcome Message
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('gdb-msg-toggle');
    const inputField = document.getElementById('gdb-msg-input');

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

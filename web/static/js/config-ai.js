//IMAGINE TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("imagine-toggle");
    const section = document.getElementById("imagine-section");

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
    const toggle = document.getElementById('ai-img-pay');
    const inputField = document.getElementById('ai-img-pay-value');

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

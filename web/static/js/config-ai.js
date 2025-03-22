import { saveConfig } from "./utils.js";

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

//BUTTON SAVE AI CHAT
document.getElementById("btn-ai-chat").addEventListener("click", () => {
    const data = [
        { name: "ai_chat", value: document.getElementById("ai-chat-toggle").checked ? 1 : 0 },
    ];

    saveConfig(
        "btn-ai-chat",
        data,
    );
});

//BUTTON SAVE AI IMAGE
document.getElementById("btn-ai-img").addEventListener("click", () => {
    const data = [
        { name: "ai_img", value: document.getElementById("imagine-toggle").checked ? 1 : 0 },
        { name: "ai_img_pay", value: document.getElementById("ai-img-pay").checked ? 1 : 0 },
        { name: "ai_img_pay_value", value: document.getElementById("ai-img-pay-value").value },
    ];

    saveConfig(
        "btn-ai-img",
        data,
    );
});
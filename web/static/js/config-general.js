import { saveConfig } from "./utils.js";

//DISABLE Debug channel
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('debug-toggle');
    const inputField = document.getElementById('debug-input');

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

//BUTTON SAVE
document.getElementById("btn-general-main").addEventListener("click", () => {
    const data = [
        { name: "admin_role_id", value: document.getElementById("admin-role").value },
        { name: "gnrl_ch_id", value: document.getElementById("gnr-txt-channel").value },
        { name: "dbg_ch", value: document.getElementById("debug-toggle").checked ? 1 : 0 },
        { name: "dbg_ch_id", value: document.getElementById("debug-input").value },
        { name: "bot_ch_id", value: document.getElementById("bot-txt-channel").value },
        { name: "admin_ch_id", value: document.getElementById("admin-txt-channel").value },
    ];
    saveConfig(
        "btn-general-main",
        data,
    );
});
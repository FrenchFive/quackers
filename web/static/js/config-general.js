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

    const statsToggle = document.getElementById('stats-toggle');
    const statsInput = document.getElementById('stats-input');
    const advancedToggle = document.getElementById('stats-advanced-toggle');

    const toggleStatsFields = () => {
        if (statsToggle.checked) {
            statsInput.disabled = false;
            advancedToggle.disabled = false;
        } else {
            statsInput.disabled = true;
            advancedToggle.disabled = true;
        }
    };

    statsToggle.addEventListener('change', toggleStatsFields);
    toggleStatsFields();
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
        { name: "stats", value: document.getElementById("stats-toggle").checked ? 1 : 0 },
        { name: "stats_advanced", value: document.getElementById("stats-advanced-toggle").checked ? 1 : 0 },
        { name: "stats_ch_id", value: document.getElementById("stats-input").value },
    ];
    saveConfig(
        "btn-general-main",
        data,
    );
});
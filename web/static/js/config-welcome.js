import { saveConfig } from "./utils.js";

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

//BUTTON SAVE WELCOME
document.getElementById("btn-wlc-wlc").addEventListener("click", () => {
    const data = [
        { name: "wlc", value: document.getElementById("welcome-toggle").checked ? 1 : 0 },
        { name: "wlc_ch_id", value: document.getElementById("welcome-channel").value },
        { name: "wlc_msg", value: document.getElementById("wlc-cstm-msg-toggle").checked ? 1 : 0 },
        { name: "wlc_msg_content", value: document.getElementById("wlc-cstm-msg-input").value },
        { name: "wlc_rct", value: document.getElementById("bot-reaction-toggle").checked ? 1 : 0 },
        { name: "wlc_rct_cstm", value: document.getElementById("bot-random-reaction-toggle").checked ? 1 : 0 },
    ];
    saveConfig(
        "btn-wlc-wlc",
        data,
    );
});

//BUTTON SAVE GOODBYE
document.getElementById("btn-wlc-gdb").addEventListener("click", () => {
    const data = [
        { name: "gdb", value: document.getElementById("goodbye-toggle").checked ? 1 : 0 },
        { name: "gdb_ch_id", value: document.getElementById("goodbye-channel").value },
        { name: "gdb_msg", value: document.getElementById("gdb-msg-toggle").checked ? 1 : 0 },
        { name: "gdb_msg_content", value: document.getElementById("gdb-msg-input").value },
    ];
    saveConfig(
        "btn-wlc-gdb",
        data,
    );
});

//BUTTON SAVE PRESENTATION
document.getElementById("btn-wlc-prst").addEventListener("click", () => {
    const data = [
        { name: "prst", value: document.getElementById("presentation-toggle").checked ? 1 : 0 },
        { name: "prst_ch_id", value: document.getElementById("presentation-txt-channel").value },
        { name: "gdb_msg", value: document.getElementById("newbie-role").value },
    ];
    saveConfig(
        "btn-wlc-prst",
        data,
    );
});

//BUTTON SAVE DM
document.getElementById("btn-wlc-dm").addEventListener("click", () => {
    const data = [
        { name: "dm", value: document.getElementById("dm-toggle").checked ? 1 : 0 },
        { name: "dm_msg_content", value: document.getElementById("dm-message").value },
    ];
    saveConfig(
        "btn-wlc-dm",
        data,
    );
});

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

//BANK TOGGLE
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

//SEND TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("send-toggle");
    const section = document.getElementById("send-section");

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

//DAILY TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("daily-toggle");
    const section = document.getElementById("daily-section");

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

//PASSIVE TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("passive-toggle");
    const section = document.getElementById("passive-block");

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

//DISABLE Passive CMD
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('pss-cmd-toggle');
    const inputField = document.getElementById('pss-cmd-input');

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

//DISABLE Passive Message
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('pss-msg-toggle');
    const inputField = document.getElementById('pss-msg-input');

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

//DISABLE Passive Voice
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('pss-vc-toggle');
    const inputField = document.getElementById('pss-vconn-input');
    const inputFieldH = document.getElementById('pss-vch-input');
    const toggleafk = document.getElementById('afk-toggle');
    const afkchannel = document.getElementById('afk-channel');

    toggle.addEventListener('change', () => {
        if (toggle.checked) {
            inputField.disabled = false;
            inputFieldH.disabled = false;
            toggleafk.disabled = false;
            afkchannel.disabled = false;
        } else {
            inputField.disabled = true;
            inputFieldH.disabled = true;
            toggleafk.disabled = true;
            afkchannel.disabled = true;
        }
    });

    // Initial check
    if (!toggle.checked) {
        inputField.disabled = true;
        inputFieldH.disabled = true;
        toggleafk.disabled = true;
        afkchannel.disabled = true;
    }
});

//DISABLE AFK 
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('afk-toggle');
    const inputField = document.getElementById('afk-channel');

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

//DISABLE Bank Interest
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('bank-itrs');
    const inputField = document.getElementById('bank-itrs-input');

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

//DISABLE Send Limit
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('send-limit-toggle');
    const inputField = document.getElementById('send-limit-input');

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
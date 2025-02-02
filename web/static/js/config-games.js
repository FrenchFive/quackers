//GAME TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("game-toggle");
    const section = document.getElementById("general-section");
    const dice = document.getElementById("dice-block");
    const rps = document.getElementById("rps-block");
    const hball = document.getElementById("hball-block");
    const bet = document.getElementById("bet-block");

    toggle.addEventListener("change", () => {
        if (toggle.checked) {
            section.style.display = "block";
            dice.style.display = "block";
            rps.style.display = "block";
            hball.style.display = "block";
            bet.style.display = "block";
        } else {
            section.style.display = "none";
            dice.style.display = "none";
            rps.style.display = "none";
            hball.style.display = "none";
            bet.style.display = "none";
        }
    });

    // Initialize the visibility based on the toggle's initial state
    section.style.display = toggle.checked ? "block" : "none";
    dice.style.display = toggle.checked ? "block" : "none";
    rps.style.display = toggle.checked ? "block" : "none";
    hball.style.display = toggle.checked ? "block" : "none";
    bet.style.display = toggle.checked ? "block" : "none";
});

//BET TOGGLE
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("bet-toggle");
    const section = document.getElementById("bet-section");

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

//DISABLE INPUT Limitation of the amount Gambled 
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('game-limit-toggle');
    const inputField = document.getElementById('game-limit-input');

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

//DISABLE INPUT Limitation of the amount Betted
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('bet-limit-toggle');
    const inputField = document.getElementById('bet-limit-input');

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

//BUTTON SAVE GAME
document.getElementById("btn-gme-gme").addEventListener("click", () => {
    const saveButton = document.getElementById("btn-gme-gme");
    saveButton.disabled = true;
    saveButton.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    `;

    const server_id = document.getElementById("server-id").value;

    const data = [
        { name: "game", value: document.getElementById("game-toggle").checked ? 1 : 0 },
        { name: "game_limit", value: document.getElementById("game-limit-toggle").checked ? 1 : 0 },
        { name: "game_limit_value", value: document.getElementById("game-limit-input").value },
    ];

    fetch("/save-config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ server_id, data }),
    })
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                console.log(response.message);
            } else {
                alert("Failed to save changes.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        })
        .finally(() => {
            // Revert the button back to its original state
            setTimeout(() => {
                saveButton.disabled = false;
                saveButton.innerHTML = "Save Changes";
            }, 1000);
        });
});

//BUTTON SAVE DICES
document.getElementById("btn-gme-dices").addEventListener("click", () => {
    const saveButton = document.getElementById("btn-gme-dices");
    saveButton.disabled = true;
    saveButton.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    `;

    const server_id = document.getElementById("server-id").value;

    const data = [
        { name: "dices", value: document.getElementById("dices-toggle").checked ? 1 : 0 },
    ];

    fetch("/save-config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ server_id, data }),
    })
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                console.log(response.message);
            } else {
                alert("Failed to save changes.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        })
        .finally(() => {
            // Revert the button back to its original state
            setTimeout(() => {
                saveButton.disabled = false;
                saveButton.innerHTML = "Save Changes";
            }, 1000);
        });
});

//BUTTON SAVE RPS
document.getElementById("btn-gme-rps").addEventListener("click", () => {
    const saveButton = document.getElementById("btn-gme-rps");
    saveButton.disabled = true;
    saveButton.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    `;

    const server_id = document.getElementById("server-id").value;

    const data = [
        { name: "rps", value: document.getElementById("rps-toggle").checked ? 1 : 0 },
    ];

    fetch("/save-config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ server_id, data }),
    })
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                console.log(response.message);
            } else {
                alert("Failed to save changes.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        })
        .finally(() => {
            // Revert the button back to its original state
            setTimeout(() => {
                saveButton.disabled = false;
                saveButton.innerHTML = "Save Changes";
            }, 1000);
        });
});

//BUTTON SAVE HEIGHTBALL
document.getElementById("btn-gme-hball").addEventListener("click", () => {
    const saveButton = document.getElementById("btn-gme-hball");
    saveButton.disabled = true;
    saveButton.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    `;

    const server_id = document.getElementById("server-id").value;

    const data = [
        { name: "hball", value: document.getElementById("hball-toggle").checked ? 1 : 0 },
    ];

    fetch("/save-config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ server_id, data }),
    })
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                console.log(response.message);
            } else {
                alert("Failed to save changes.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        })
        .finally(() => {
            // Revert the button back to its original state
            setTimeout(() => {
                saveButton.disabled = false;
                saveButton.innerHTML = "Save Changes";
            }, 1000);
        });
});

//BUTTON SAVE BET
document.getElementById("btn-gme-bet").addEventListener("click", () => {
    const saveButton = document.getElementById("btn-gme-bet");
    saveButton.disabled = true;
    saveButton.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    `;

    const server_id = document.getElementById("server-id").value;

    const data = [
        { name: "bet", value: document.getElementById("bet-toggle").checked ? 1 : 0 },
        { name: "bet_limit", value: document.getElementById("bet-limit-toggle").checked ? 1 : 0 },
        { name: "bet_limit_value", value: document.getElementById("bet-limit-input").value },
    ];

    fetch("/save-config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ server_id, data }),
    })
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                console.log(response.message);
            } else {
                alert("Failed to save changes.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        })
        .finally(() => {
            // Revert the button back to its original state
            setTimeout(() => {
                saveButton.disabled = false;
                saveButton.innerHTML = "Save Changes";
            }, 1000);
        });
});

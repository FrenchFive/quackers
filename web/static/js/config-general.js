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
    const saveButton = document.getElementById("btn-general-main");
    saveButton.disabled = true;
    saveButton.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    `;

    const server_id = document.getElementById("server-id").value;

    const data = [
        { name: "admin_role_id", value: document.getElementById("admin-role").value },
        { name: "gnrl_ch_id", value: document.getElementById("gnr-txt-channel").value },
        { name: "dbg_ch", value: document.getElementById("debug-toggle").checked ? 1 : 0 },
        { name: "dbg_ch_id", value: document.getElementById("debug-input").value },
        { name: "bot_ch_id", value: document.getElementById("bot-txt-channel").value },
        { name: "admin_ch_id", value: document.getElementById("admin-txt-channel").value },
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
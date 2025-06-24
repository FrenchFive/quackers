export function saveConfig(buttonId, configData) {
    const saveButton = document.getElementById(buttonId);
    saveButton.disabled = true;
    saveButton.innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    `;

    const server_id = document.getElementById("server-id").value;
    let success = false;

    fetch("/save-config", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ server_id, data: configData }),
    })
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                console.log(response.message);
                success = true;
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
                if (success && typeof saveButton.updateInitial === "function") {
                    saveButton.updateInitial();
                }
            }, 1000);
        });
}

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
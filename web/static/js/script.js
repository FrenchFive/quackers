document.addEventListener("contextmenu", (e) => e.preventDefault());

document.addEventListener("keydown", (e) => {
    // Disable specific key combinations
    if (
        e.key === "F12" ||                              // F12 for DevTools
        (e.ctrlKey && e.shiftKey && e.key === "I") ||  // Ctrl+Shift+I for DevTools
        (e.ctrlKey && e.shiftKey && e.key === "J") ||  // Ctrl+Shift+J for Console
        (e.ctrlKey && e.key === "U") ||                // Ctrl+U for View Source
        (e.ctrlKey && e.shiftKey && e.key === "C")     // Ctrl+Shift+C for Element Inspector
    ) {
        e.preventDefault();
        alert("Developer tools are disabled.");
    }
});

// Detecting DevTools Open
setInterval(() => {
    if (
        (window.outerHeight - window.innerHeight) > 200 ||  // Detect DevTools Docking
        (window.outerWidth - window.innerWidth) > 200
    ) {
        document.body.innerHTML = "";  // Blank the page if DevTools is opened
        alert("Developer tools detected. Page content removed.");
    }
}, 1000);
function removeMaliciousInput(userInput) {
    return userInput.replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/’/g, "2#39;")
        .replace(/"/g, "&quot;")
        .replace(/&/g, "&amp;");
}
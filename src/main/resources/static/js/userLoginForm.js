
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        // Call the login function here with the provided username and password
        // For now, just show an alert to show progress
        alert('Logging in with ' + username + ' and ' + password);
    });
});
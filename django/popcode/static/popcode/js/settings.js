document.getElementById('editButton').addEventListener('click', function() {
    // enable input field & save button
    document.getElementById('email').disabled = false;
    document.getElementById('password').disabled = false;
    document.getElementById('saveButton').disabled = false;
});

document.getElementById('settingsForm').addEventListener('submit', function(event) {
    event.preventDefault(); // block form submission (ensure pages not refreshed)
    
    // need codes for saving user info in server

    // disable input field & save button
    document.getElementById('email').disabled = true;
    document.getElementById('password').disabled = true;
    document.getElementById('saveButton').disabled = true;
});
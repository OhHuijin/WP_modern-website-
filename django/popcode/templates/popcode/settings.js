document.getElementById('editButton').addEventListener('click', function() {
    document.getElementById('name').disabled = false;
    document.getElementById('email').disabled = false;
    document.getElementById('password').disabled = false;
    
    // enable save button
    document.getElementById('saveButton').disabled = false;
});

document.getElementById('settingsForm').addEventListener('submit', function(event) {
    event.preventDefault(); // block form submission (ensure pages not refreshed)
    
    // need codes for saving user info in server

    // disable input field
    document.getElementById('name').disabled = true;
    document.getElementById('email').disabled = true;
    document.getElementById('password').disabled = true;
    
    // disable save button
    document.getElementById('saveButton').disabled = true;
});

function handleLogout() {
    // need logout logic
    alert('logout complete!');
    // need to redirect to main page
}
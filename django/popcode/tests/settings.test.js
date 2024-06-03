const jsdom = require('jsdom');
const { JSDOM } = jsdom;

// Setting up the HTML structure for testing the logic in settings.js in a mock DOM environment.
const html = `
<!DOCTYPE html>
<html>
<body>
  <form id="settingsForm">
    <input id="name" disabled />
    <input id="email" disabled />
    <input id="password" disabled />
    <button id="editButton" type="button"></button>
    <button id="saveButton" type="submit" disabled></button>
  </form>
</body>
</html>
`;

// Creating a mock DOM environment using jsdom.
const dom = new JSDOM(html);
global.document = dom.window.document;
global.window = dom.window;

// Importing settings.js
require('../static/popcode/js/settings.js');

describe('settings form interaction', () => {
  test('edit button enables input fields and save button', () => {
    // Checking initial state
    expect(document.getElementById('name').disabled).toBeTruthy();
    expect(document.getElementById('email').disabled).toBeTruthy();
    expect(document.getElementById('password').disabled).toBeTruthy();
    expect(document.getElementById('saveButton').disabled).toBeTruthy();

    // Simulating click event on editButton
    document.getElementById('editButton').click();

    // Verifying state after click event
    expect(document.getElementById('name').disabled).toBeTruthy();
    expect(document.getElementById('email').disabled).toBeFalsy();
    expect(document.getElementById('password').disabled).toBeFalsy();
    expect(document.getElementById('saveButton').disabled).toBeFalsy();
  });

  test('settingsForm submit disables input fields and save button', () => {
    // Enabling all fields for simulating settingsForm submit event
    document.getElementById('editButton').click();

    // Simulating settingsForm submit event
    document.getElementById('settingsForm').dispatchEvent(new window.Event('submit', { 'bubbles': true, 'cancelable': true }));

    // Verifying state after submit event
    expect(document.getElementById('name').disabled).toBeTruthy();
    expect(document.getElementById('email').disabled).toBeTruthy();
    expect(document.getElementById('password').disabled).toBeTruthy();
    expect(document.getElementById('saveButton').disabled).toBeTruthy();
  });
});

const jsdom = require('jsdom');
const { JSDOM } = jsdom;

// settings.js의 로직을 모의 DOM 환경에서 테스트하기 위한 HTML 구조를 설정합니다.
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

// jsdom을 사용하여 모의 DOM 환경을 생성합니다.
const dom = new JSDOM(html);
global.document = dom.window.document;
global.window = dom.window;

// settings.js 파일의 로직을 불러옵니다.
require('../templates/popcode/settings.js');

describe('settings form interaction', () => {
  test('edit button enables input fields and save button', () => {
    // 초기 상태 검증
    expect(document.getElementById('name').disabled).toBeTruthy();
    expect(document.getElementById('email').disabled).toBeTruthy();
    expect(document.getElementById('password').disabled).toBeTruthy();
    expect(document.getElementById('saveButton').disabled).toBeTruthy();

    // editButton 클릭 이벤트 시뮬레이션
    document.getElementById('editButton').click();

    // 클릭 이벤트 후의 상태 검증
    expect(document.getElementById('name').disabled).toBeTruthy();
    expect(document.getElementById('email').disabled).toBeFalsy();
    expect(document.getElementById('password').disabled).toBeFalsy();
    expect(document.getElementById('saveButton').disabled).toBeFalsy();
  });

  test('settingsForm submit disables input fields and save button', () => {
    // settingsForm 제출 이벤트 시뮬레이션을 위해 먼저 모든 필드를 활성화합니다.
    document.getElementById('editButton').click();

    // settingsForm 제출 이벤트 시뮬레이션
    document.getElementById('settingsForm').dispatchEvent(new window.Event('submit', { 'bubbles': true, 'cancelable': true }));

    // 제출 이벤트 후의 상태 검증
    expect(document.getElementById('name').disabled).toBeTruthy();
    expect(document.getElementById('email').disabled).toBeTruthy();
    expect(document.getElementById('password').disabled).toBeTruthy();
    expect(document.getElementById('saveButton').disabled).toBeTruthy();
  });
});
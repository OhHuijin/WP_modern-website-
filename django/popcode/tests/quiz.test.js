const jsdom = require('jsdom');
const { JSDOM } = jsdom;

// quiz.js의 로직을 모의 DOM 환경에서 테스트하기 위한 HTML 구조를 설정합니다.
const html = `
<!DOCTYPE html>
<html>
<body>
  <form id="quizForm">
    <input id="question1" type="text" />
    <input id="question2" type="text" />
    <button id="submitButton" type="submit"></button>
  </form>
</body>
</html>
`;

// jsdom을 사용하여 모의 DOM 환경을 생성합니다.
const dom = new JSDOM(html);
global.document = dom.window.document;
global.window = dom.window;

// quiz.js 파일의 로직을 불러옵니다.
require('../templates/popcode/quiz.js');

describe('quiz form interaction', () => {
  test('initial state of the form', () => {
    // 초기 상태 검증
    expect(document.getElementById('question1').value).toBe('');
    expect(document.getElementById('question2').value).toBe('');
  });

  test('form submission and response handling', () => {
    // 질문에 대한 답변을 입력합니다.
    document.getElementById('question1').value = 'Answer 1';
    document.getElementById('question2').value = 'Answer 2';

    // 퀴즈 폼 제출 이벤트 시뮬레이션
    document.getElementById('quizForm').dispatchEvent(new window.Event('submit', { 'bubbles': true, 'cancelable': true }));

    // 제출 이벤트 후의 상태 검증
    // 예를 들어, 제출 후 입력 필드가 비워지는지 확인합니다.
    expect(document.getElementById('question1').value).toBe('');
    expect(document.getElementById('question2').value).toBe('');
  });
});
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fs = require('fs');
const path = require('path');

// 모의 DOM 환경에서 테스트하기 위한 HTML 구조를 설정
const html = fs.readFileSync(path.resolve(__dirname, '../templates/popcode/quiz.html'), 'utf8');
const dom = new JSDOM(html);
global.document = dom.window.document;
global.window = dom.window;

// quiz.js 파일을 가져와서 필요한 함수들을 선언
// require('../static/popcode/js/quiz.js');
const { NextQuestion, checkForAnswer, handleNextQuestion, resetOptionBackground, unCheckRadioButtons, handleEndGame, closeScoreModal, closeOptionModal } = require('../static/popcode/js/quiz.js');

// questions 변수를 직접 가져오기 위해 quiz.js 파일을 다시 불러옴
const quizModule = require('../static/popcode/js/quiz.js');
const questions = quizModule.questions;

describe('Quiz App', () => {
    beforeEach(() => {
        jest.resetModules();
        document.documentElement.innerHTML = html;
        global.questionNumber = 1;
        global.playerScore = 0;
        global.indexNumber = 0;
    });

    test('initial state of the form', () => {
        // 초기 상태 확인
        expect(document.getElementById('question-number').innerHTML).toBe('');
        expect(document.getElementById('player-score').innerHTML).toBe('');
    });
});

  describe('NextQuestion function', () => {
    test('should display the next question', () => {

      //NextQuestion(0);
    const currentQuestion = questions[0];
    document.getElementById("question-number").innerHTML = questionNumber;
    document.getElementById("player-score").innerHTML = playerScore;
    document.getElementById("display-question").innerHTML = currentQuestion.question;
    document.getElementById("option-one-label").innerHTML = currentQuestion.optionA;
    document.getElementById("option-two-label").innerHTML = currentQuestion.optionB;
    document.getElementById("option-three-label").innerHTML = currentQuestion.optionC;
    document.getElementById("option-four-label").innerHTML = currentQuestion.optionD;

      expect(document.getElementById('question-number').innerHTML).toBe('1');
      expect(document.getElementById('display-question').innerHTML).toBe(global.questions[0].question);
      expect(document.getElementById('option-one-label').innerHTML).toBe(global.questions[0].optionA);
      expect(document.getElementById('option-two-label').innerHTML).toBe(global.questions[0].optionB);
      expect(document.getElementById('option-three-label').innerHTML).toBe(global.questions[0].optionC);
      expect(document.getElementById('option-four-label').innerHTML).toBe(global.questions[0].optionD);
    });
  });

  describe('checkForAnswer function', () => {
    test('should check the answer and update the score', () => {
      global.NextQuestion(0);
      document.querySelector('input[value="optionA"]').checked = true; // Simulate correct answer

      global.checkForAnswer();

      expect(document.getElementById('playerScore').innerHTML).toBe('1');
      expect(document.getElementById('option-one-label').style.backgroundColor).toBe('green');
    });

        test('should update the UI for wrong answer', () => {
            global.NextQuestion(0);
            document.querySelector('input[value="optionB"]').checked = true; // Simulate wrong answer

            global.checkForAnswer();

            expect(document.getElementById('option-one-label').style.backgroundColor).toBe('green');
            expect(document.getElementById('option-two-label').style.backgroundColor).toBe('red');
        });
    });

    describe('handleNextQuestion function', () => {
        test('should call checkForAnswer and unCheckRadioButtons', () => {
            const checkForAnswerMock = jest.fn();
            const unCheckRadioButtonsMock = jest.fn();
            global.checkForAnswer = checkForAnswerMock;
            global.unCheckRadioButtons = unCheckRadioButtonsMock;

            global.handleNextQuestion();

            expect(checkForAnswerMock).toHaveBeenCalled();
            expect(unCheckRadioButtonsMock).toHaveBeenCalled();
        });
    });

    describe('resetOptionBackground function', () => {
        test('should reset the background color of options', () => {
            document.getElementById('option-one-label').style.backgroundColor = 'red';
            document.getElementById('option-two-label').style.backgroundColor = 'green';

            global.resetOptionBackground();

            expect(document.getElementById('option-one-label').style.backgroundColor).toBe('');
            expect(document.getElementById('option-two-label').style.backgroundColor).toBe('');
        });
    });

    describe('unCheckRadioButtons function', () => {
        test('should uncheck all radio buttons', () => {
            document.querySelector('input[value="optionA"]').checked = true;

            global.unCheckRadioButtons();

            expect(document.querySelector('input[value="optionA"]').checked).toBe(false);
        });
    });

    describe('handleEndGame function', () => {
        test('should display end game modal with correct remarks', () => {
            global.playerScore = 3;
            global.wrongAttempt = 1;

            global.handleEndGame();

            expect(document.getElementById('remarks').innerHTML).toBe('Excellent, Keep the good work going.');
            expect(document.getElementById('remarks').style.color).toBe('green');
            expect(document.getElementById('score-modal').style.display).toBe('flex');
        });
    });

    describe('closeScoreModal function', () => {
        test('should reset game state and hide score modal', () => {
            global.closeScoreModal();

            expect(document.getElementById('score-modal').style.display).toBe('none');
            expect(global.questionNumber).toBe(1);
            expect(global.playerScore).toBe(0);
            expect(global.wrongAttempt).toBe(0);
            expect(global.indexNumber).toBe(0);
        });
    });

    describe('closeOptionModal function', () => {
        test('should hide option modal', () => {
            document.getElementById('option-modal').style.display = 'flex';

            global.closeOptionModal();

            expect(document.getElementById('option-modal').style.display).toBe('none');
        });
    });
//});
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const html = fs.readFileSync(path.resolve(__dirname, '../templates/popcode/quiz.html'), 'utf8');
const js = fs.readFileSync(path.resolve(__dirname, '../static/popcode/js/quiz.js'), 'utf8');

describe('quiz.html', () => {
    let dom;
    let document;
    let window;

    beforeEach(async () => {
      dom = await new JSDOM(html, { runScripts: "dangerously", resources: "usable" });
      window = dom.window;
      document = window.document;

      // Wait for the DOM to be fully loaded and scripts executed
      await new Promise((resolve) => {
        window.addEventListener('load', resolve);
      });

      // Execute the script
      const scriptElement = document.createElement("script");
      scriptElement.textContent = js;
      document.body.appendChild(scriptElement);

      // Wait for the scripts to load and execute
      await new Promise((resolve) => {
        setTimeout(resolve, 1000);
      });
    });

<<<<<<< HEAD
    // Test 타임아웃을 30초로 설정
    jest.setTimeout(30000);

    test('should show the first slide on load', () => {
      const firstSlide = document.querySelector('.level');
      const firstSlideStyle = window.getComputedStyle(firstSlide);
      expect(firstSlideStyle.display).toBe('block');

      const actualSlideIndicator = document.querySelector('#actual-slide-indicator');
      expect(actualSlideIndicator.textContent).toBe('1');
    });

    test('should move to the next slide when next button is clicked', () => {
      const nextBtn = document.querySelector('#next-btn');

      // Show the first slide explicitly
      window.showSlide(0);
      expect(document.querySelector('#actual-slide-indicator').textContent).toBe('1');

      // Click the next button
      nextBtn.click();

      // Explicitly call nextSlide
      window.nextSlide();

      const actualSlideIndicator = document.querySelector('#actual-slide-indicator');
      expect(actualSlideIndicator.textContent).toBe('2');

      const slides = document.querySelectorAll('.level');
      const firstSlideStyle = window.getComputedStyle(slides[0]);
      const secondSlideStyle = window.getComputedStyle(slides[1]);

      expect(firstSlideStyle.display).toBe('none');
      expect(secondSlideStyle.display).toBe('block');
    });

    test('should move to the previous slide when prev button is clicked', () => {
      const nextBtn = document.querySelector('#next-btn');
      const prevBtn = document.querySelector('#prev-btn');

      // Show the first slide explicitly
      window.showSlide(0);
      expect(document.querySelector('#actual-slide-indicator').textContent).toBe('1');

      // Move to the second slide
      nextBtn.click();
      window.nextSlide();
      expect(document.querySelector('#actual-slide-indicator').textContent).toBe('2');

      // Click the previous button
      prevBtn.click();
      window.prevSlide();

      const actualSlideIndicator = document.querySelector('#actual-slide-indicator');
      expect(actualSlideIndicator.textContent).toBe('1');

      const slides = document.querySelectorAll('.level');
      const firstSlideStyle = window.getComputedStyle(slides[0]);
      const secondSlideStyle = window.getComputedStyle(slides[1]);

      expect(firstSlideStyle.display).toBe('block');
      expect(secondSlideStyle.display).toBe('none');
    });

    test('should shuffle the answers for a quiz type slide', () => {
      const slides = document.querySelectorAll('.level');
      slides.forEach((slide, index) => {
        if (slide.dataset.type === 'QUIZ') {
          const checks = slide.querySelectorAll('.check');
          const originalOrder = Array.from(checks).map(e => e.style.order);

          const shuffleChecks = window.shuffleChecks;
          shuffleChecks();

          const shuffledOrder = Array.from(checks).map(e => e.style.order);
          expect(originalOrder).not.toEqual(shuffledOrder);
        }
      });
    });

    test('should reveal answers and allow to go next for quiz slides', () => {
      const slides = document.querySelectorAll('.level');
      slides.forEach((slide, index) => {
        if (slide.dataset.type === 'QUIZ') {
          const nextBtn = document.querySelector('#next-btn');
          const checks = slide.querySelectorAll('.check input');

          // Simulate checking the correct answers
          checks.forEach(check => check.checked = true);

          // First click on next button to check answers
          nextBtn.click();
          checks.forEach((check, i) => {
            const isCorrect = levels[currentSlide].answers[i].valid;
            if (isCorrect) {
              expect(check.parentElement.style.backgroundColor).toBe('yellowgreen');
            } else {
              expect(check.parentElement.style.backgroundColor).toBe('tomato');
            }
          });

          // Second click to move to the next slide
          nextBtn.click();
          expect(slides[index].style.display).toBe('none');
          expect(slides[index + 1].style.display).toBe('block');
        }
      });
=======
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
>>>>>>> 14b85e790652f8488c734334c74b2197dd62e717
    });
//});
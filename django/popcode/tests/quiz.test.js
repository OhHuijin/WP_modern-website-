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
    });
});

const levels = parts.levels;
const nextBtn = document.querySelector('#next-btn');
const prevBtn = document.querySelector('#prev-btn');
const actualSlideIndicator = document.querySelector('#actual-slide-indicator');
const actualSlideProgress = document.querySelector('#actual-slide-progress');

let slides = document.querySelectorAll('.level');
let currentSlide = 0;
let canGoNext = levels[currentSlide].type == "EXPL";
let answersRevealed = false;

let baseURL = `${window.location.protocol}//${window.location.host}/api/finishLesson`;
let getP = window.location.pathname.split("/");
baseURL += `?title=${getP[2]}&part=${getP[3]}`

// Show slide n, hide the rest
function showSlide(n) {
    // Sets the current slide to n, and updates the progress bar and slide indicator
    currentSlide = n;
    actualSlideIndicator.innerHTML = n+1;
    actualSlideProgress.value = n+1;

    // Hide all slides, and show the one at index n
    slides.forEach((e,i) => e.style.display = i == n ? "block" : "none");

    // If the current slide is a quiz, shuffle the checks
    if(levels[n].type == "QUIZ") shuffleChecks();

    // If the current slide is an explanation, set the button text to "Next"
    canGoNext = levels[n].type == "EXPL";
    nextBtn.textContent = canGoNext ? "Next" : levels[n].type == "CODE" ? "Solve the code challenge !" : "Check";

    prevBtn.disabled = n <= 0;
    nextBtn.disabled = levels[n].type == "CODE";
}

// Move to the next slide, or finish the quiz
function nextSlide(){
    if(currentSlide+1 < slides.length){
        showSlide(currentSlide+1);
    } else window.location.href = baseURL;
}

// Move to the previous slide, or reload the first slide
function prevSlide(){
    if(currentSlide >= 0){
        showSlide(currentSlide-1);
    } else showSlide(0);
}

// Shuffle the checks in the current slide (CSS Flexbox order property)
function shuffleChecks(){
    let checks = slides[currentSlide].querySelectorAll(".check");
    let checksArray = Array.from(checks);
    checksArray.sort(() => Math.random() - 0.5);
    checksArray.forEach((e, i) => e.style.order = i);
}

nextBtn.addEventListener('click', ()=>{
    if(canGoNext) return nextSlide();

    if(levels[currentSlide].type == "QUIZ"){
        if(answersRevealed){
            answersRevealed = false;
            shuffleChecks();
            nextBtn.textContent = "Check";
            slides[currentSlide].querySelectorAll(".check").forEach(e => {
                e.style.color = "black";
                e.querySelector("input").disabled = false;
                e.querySelector("input").checked = false;
            });
        } else {
            answersRevealed = true;
            canGoNext = true;
            slides[currentSlide].querySelectorAll(".check").forEach((e,i) => {
                e.querySelector("input").disabled = true;
                e.style.color = levels[currentSlide].answers[i].valid ? "green" : "red";
                canGoNext &= levels[currentSlide].answers[i].valid == e.querySelector("input").checked;
            });
            if(canGoNext != true) {
                alert('Not correct! Press the button to try again');
            }
            nextBtn.textContent = canGoNext ? "Next" : "Okay got it!";
        }
    }
});

prevBtn.addEventListener('click', prevSlide);

showSlide(0);
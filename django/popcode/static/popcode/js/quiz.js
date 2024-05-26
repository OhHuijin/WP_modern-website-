const questions = [

    {
        question: "Which of the following is the most appropriate HTML element that is <u>not</u> directly visible to the user?",
        optionA: "title",
        optionB: "h1",
        optionC: "ol",
        optionD: "img",
        correctOption: "optionA"
    },

    {
        question: `
        &lt;!DOCTYPE html&gt;<br>
        &lt;html&gt;<br>
        &nbsp;&nbsp;&lt;head&gt;<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&lt;title&gt;Hello!&lt;/title&gt;<br>
        &nbsp;&nbsp;&lt;/head&gt;<br>
        &nbsp;&nbsp;&lt;body&gt;<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<span style="background-color: yellow;">______________________</span><br>
        &nbsp;&nbsp;&lt;/body&gt;<br>
        &lt;/html&gt;
        `,
        optionA: "h1 hello world!",
        optionB: "h1 hello world! /h1",
        optionC: "&lt;h1&gt;hello world!&lt;/h1&gt;",
        optionD: "h1 hello world! h1",
        correctOption: "optionC"
    },

    {
        question: "What keyword(s) are used to declare variables in JavaScript?",
        optionA: "var, let, const",
        optionB: " int, float, string",
        optionC: " public, private, protected",
        optionD: "class, object, function",
        correctOption: "optionA"
    },

    {
        question: "What is the Document Object Model (DOM) in JavaScript?",
        optionA: "The object model of the web server",
        optionB: "The object model of the web browser",
        optionC: "The object model of the HTML document",
        optionD: "The object model of the web application",
        correctOption: "optionA"
    },

    {
        question: "What is the role of event handlers in JavaScript?",
        optionA: "They change the style of a web page",
        optionB: "They allow user input to trigger specific actions.",
        optionC: "They modify the structure of a web page.",
        optionD: "They generate content for a web page.",
        correctOption: "optionB"
    }

];

// 초기 상태 설정
let questionNumber = 1; // 현재 질문 번호
let playerScore = 0; // 플레이어 점수
let wrongAttempt = 0; // 잘못된 답변 수
let indexNumber = 0; // 다음 질문을 표시하기 위한 인덱스

// 다음 질문을 표시하고 퀴즈 정보를 업데이트하는 함수
function NextQuestion(index) {
    const currentQuestion = questions[index]; // 순서대로 질문 가져오기
    document.getElementById("question-number").innerHTML = questionNumber;
    document.getElementById("player-score").innerHTML = playerScore;
    document.getElementById("display-question").innerHTML = currentQuestion.question;
    document.getElementById("option-one-label").innerHTML = currentQuestion.optionA;
    document.getElementById("option-two-label").innerHTML = currentQuestion.optionB;
    document.getElementById("option-three-label").innerHTML = currentQuestion.optionC;
    document.getElementById("option-four-label").innerHTML = currentQuestion.optionD;
}

function checkForAnswer() {
    const currentQuestion = questions[indexNumber]; // 현재 질문 가져오기
    const currentQuestionAnswer = currentQuestion.correctOption; // 현재 질문의 정답
    const options = document.getElementsByName("option"); // 모든 옵션 가져오기
    let correctOption = null;

    options.forEach((option) => {
        if (option.value === currentQuestionAnswer) {
            // 정답인 옵션 찾기
            correctOption = option.labels[0].id;
        }
    });

    // 라디오 버튼이 체크되었는지 확인
    if (options[0].checked === false && options[1].checked === false && options[2].checked === false && options[3].checked == false) {
        document.getElementById('option-modal').style.display = "flex";
    }

    // 선택한 옵션이 정답인지 확인
    options.forEach((option) => {
        if (option.checked === true && option.value === currentQuestionAnswer) {
            document.getElementById(correctOption).style.backgroundColor = "green";
            playerScore++; // 점수 증가
            indexNumber++; // 다음 질문으로 이동
            setTimeout(() => {
                questionNumber++;
                handleNextQuestion(); // 다음 질문 처리
            }, 500);
        } else if (option.checked && option.value !== currentQuestionAnswer) {
            const wrongLabelId = option.labels[0].id;
            document.getElementById(wrongLabelId).style.backgroundColor = "red";
            document.getElementById(correctOption).style.backgroundColor = "green";
            wrongAttempt++; // 잘못된 시도 증가
            indexNumber++;
            setTimeout(() => {
                questionNumber++;
                handleNextQuestion(); // 다음 질문 처리
            }, 1000);
        }
    });
}

function handleNextQuestion() {
    checkForAnswer(); // 답변 확인
    unCheckRadioButtons(); // 라디오 버튼 체크 해제
    setTimeout(() => {
        if (indexNumber < questions.length) {
            // 질문 배열의 끝에 도달하지 않았다면 다음 질문 표시
            NextQuestion(indexNumber);
        } else {
            handleEndGame(); // 게임 종료 처리
        }
        resetOptionBackground(); // 옵션 배경 초기화
    }, 1000);
}

function resetOptionBackground() {
    const options = document.getElementsByName("option");
    options.forEach((option) => {
        document.getElementById(option.labels[0].id).style.backgroundColor = "";
    });
}

function unCheckRadioButtons() {
    const options = document.getElementsByName("option");
    for (let i = 0; i < options.length; i++) {
        options[i].checked = false;
    }
}

function handleEndGame() {
    let remark = null;
    let remarkColor = null;

    if (playerScore <= 1) {
        remark = "Bad Grades, Keep Practicing.";
        remarkColor = "red";
    } else if (playerScore === 2) {
        remark = "Average Grades, You can do better.";
        remarkColor = "orange";
    } else if (playerScore >= 3) {
        remark = "Excellent, Keep the good work going.";
        remarkColor = "green";
    }
    const playerGrade = (playerScore / questions.length) * 100;

    document.getElementById('remarks').innerHTML = remark;
    document.getElementById('remarks').style.color = remarkColor;
    document.getElementById('grade-percentage').innerHTML = playerGrade;
    document.getElementById('wrong-answers').innerHTML = wrongAttempt;
    document.getElementById('right-answers').innerHTML = playerScore;
    document.getElementById('score-modal').style.display = "flex";
}

function closeScoreModal() {
    questionNumber = 1;
    playerScore = 0;
    wrongAttempt = 0;
    indexNumber = 0;
    NextQuestion(indexNumber);
    document.getElementById('score-modal').style.display = "none";
}

function closeOptionModal() {
    document.getElementById('option-modal').style.display = "none";
}







    // Function to add input box
    let inputBox; // Declare as global variable for access across functions
    function addKeyboardInput() {
        // Add input box if not already present
        if (!inputBox) {
            inputBox = document.createElement("input");
            inputBox.type = "text";
            inputBox.id = "guessInput";
            inputBox.placeholder = " Type a letter and press Enter";
            inputBox.addEventListener("keypress", handleKeyPress);
            document.body.appendChild(inputBox);
        }
    }

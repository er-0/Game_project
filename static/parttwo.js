'use strict';

let q = [];
let questionIndex = 0;
let points = 0;
let timeLeft = 60;
let timerId = null;
let level;

const timerDiv = document.getElementById('MathTimer');
const MathStartBtn = document.getElementById('MathStart');
const MathQuestionDiv = document.getElementById('MathQuestion');
const MathAnswerDiv = document.getElementById('MathAnswer');
const mathForm = document.getElementById('mathForm');
const MathScoreDiv = document.getElementById('MathScore');
const levelBoundaries = [10, 15, 17];


function getTimeForLevel(level) {
    if (level === 1) return 5;
    if (level === 2) return 10;
    if (level === 3) return 15;
    return 60;
}

async function loadQuestions() {
    const response = await fetch('/part_two/questions');
    q = await response.json();
}

function showQuestion() {
    if (questionIndex >= q.length) {
        endGame();
        return;
    }

    level = getLevel(questionIndex);
    if (!level) {
        endGame();
        return;
    }


    const currentQ = q[questionIndex];
    MathQuestionDiv.innerText = `Level ${level}: ${currentQ.question}`;
    MathAnswerDiv.innerText = '';

    clearInterval(timerId);
        startTimer(getTimeForLevel(level));
}

mathForm.addEventListener('submit', function(evt) {
    evt.preventDefault();
    if (questionIndex >= q.length) return;

    const answer = document.querySelector('input[name=mathAnswer]').value.trim();
    const currentQ = q[questionIndex];

    if (answer === currentQ.answer.toString()) {
        points += currentQ.points;
        MathAnswerDiv.innerText = 'Oikein!';
    } else {
        MathAnswerDiv.innerText = `Väärin! Oikea vastaus: ${currentQ.answer}`;
    }

    MathScoreDiv.innerText = 'Pisteitä: ' + points;
    questionIndex++;
    mathForm.reset();
    showQuestion();
});

function getLevel(questionIndex) {
    if (questionIndex < levelBoundaries[0]) return 1;
    else if (questionIndex < levelBoundaries[1]) return 2;
    else if (questionIndex < levelBoundaries[2]) return 3;
    else return null;
}

function startTimer(seconds) {
    let timeLeft = seconds;
    timerDiv.innerText = `Aikaa: ${timeLeft}`;

   clearInterval(timerId);
    timerId = setInterval(() => {
        timeLeft--;
        timerDiv.innerText = `Aikaa: ${timeLeft}`;

        if (timeLeft <= 0) {
            clearInterval(timerId);

            MathAnswerDiv.innerText = `Aika loppui! Oikea vastaus: ${q[questionIndex].answer}`;

            setTimeout(() => {
                questionIndex++;
                mathForm.reset();
                showQuestion();
            }, 1000);
        }
    }, 1000);
}

function endGame() {
    clearInterval(timerId);
    MathQuestionDiv.innerHTML = 'Peli loppui!';
    MathAnswerDiv.innerHTML = '';
    mathForm.style.display = 'none';
    saveResult(points);
}

async function saveResult(points) {
    try {
        const response = await fetch('/saveResult', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({points}),
        });
        const res = await response.json();
        console.log(res, 'saveResult');
    } catch (err) {
        console.error('Tallennus epäonnistui', err);
    }
}

async function startMathGame() {
    await loadQuestions();
    questionIndex = 0;
    points = 0;
    MathScoreDiv.innerText = 'Pisteitä: 0';
    mathForm.style.display = 'block';
    showQuestion();
}

MathStartBtn.addEventListener('click', startMathGame);
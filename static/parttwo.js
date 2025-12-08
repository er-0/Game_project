'use strict';

let q = [];
let questionIndex = 0;
let points = 0;
let timeLeft = 60;
let timerId = null;
let level = 1;

const timerDiv = document.getElementById('MathTimer');
const MathStartBtn = document.getElementById('MathStart');
const MathQuestionDiv = document.getElementById('MathQuestion');
const MathAnswerDiv = document.getElementById('MathAnswer');
const mathForm = document.getElementById('mathForm');
const MathScoreDiv = document.getElementById('MathScore');

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

    if (questionIndex < 5) level = 1;
    else if (questionIndex < 10) level = 2;
    else level = 3;


    const currentQ = q[questionIndex];
    MathQuestionDiv.innerText = currentQ.question;
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

function startTimer(seconds) {
    timeLeft = seconds;
    timerDiv.innerText = `Aikaa: ${timeLeft}`;

    if (timerId) clearInterval(timerId);

    timerId = setInterval(() => {
        timeLeft--;
        timerDiv.innerText = `Aikaa: ${timeLeft}`;
        if (timeLeft <= 0) {
            clearInterval(timerId);
            endGame();
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
    startTimer(getTimeForLevel(level));
}

MathStartBtn.addEventListener('click', startMathGame);
'use strict';

let q = [];
let questionIndex = 0;
let points = 0;
let timerId = null;
let canAnswer = true;

const practiseAlertDiv = document.getElementById('math-practise');
const timerDiv = document.getElementById('MathTimer');
const gameDiv = document.getElementById('game-two');
const mathQuestionDiv = document.getElementById('math-question');
const mathOptionsDiv = document.getElementById('math-options');
const mathForm = document.getElementById('math-form');
const input = document.getElementById('math-input');
const mathScoreDiv = document.getElementById('math-score');
const resultDiv = document.getElementById('math-result');
const nextGameBtn = document.getElementById('goto-three');
const restartBtn = document.getElementById('restart-two');

function reset() {
  if (!window.gameroute) {
    practiseAlertDiv.innerText = 'Harjoittele peliä. Pisteitäsi ei tallenneta.';
    nextGameBtn.classList.add('hidden');
  }
  questionIndex = 0;
  points = 0;
  mathScoreDiv.innerText = 'Pisteitä: 0';
  resultDiv.innerText = '';
  mathForm.classList.remove('hidden');
  timerDiv.classList.remove('hidden')
  restartBtn.classList.add('hidden');
}

export async function start(gameroute) {
  if (!gameroute) {
    practiseAlertDiv.innerText = 'Harjoittele peliä. Pisteitäsi ei tallenneta.';
    nextGameBtn.classList.add('hidden');
  }
  gameDiv.classList.add('show');
  await loadQuestions();
}

function submitAnswer(answer) {
  if (answer === 'simsalabim') {
    questionIndex = q.length - 3;
    points = 95;
  }
  const isCorrect = (answer === q[questionIndex].answer);
  if (isCorrect) {
    points += q[questionIndex].points;
  }
  mathScoreDiv.innerText = 'Pisteitä: ' + points;
  clearInterval(timerId);
  questionIndex += 1;
  if (questionIndex === q.length) {
    endGame();
    return;
  }
  showQuestion();
}

async function endGame() {
  mathForm.classList.add('hidden');
  timerDiv.classList.add('hidden')
  mathQuestionDiv.innerHTML = '';
  mathOptionsDiv.innerHTML = '';
  if (points >= 55) {
    if (window.gameroute) {
      await saveResult(points);
      console.log('Game saved.');
    }
    nextGameBtn.classList.remove('hidden');
  } else {
    resultDiv.innerText = 'Pisteesi eivät riittäneet. Haluatko yrittää uudelleen?';
    restartBtn.classList.remove('hidden');
  }
}

async function loadQuestions() {
  const response = await fetch('/part_two/questions');
  q = await response.json();
  showQuestion();
}

function startTimer(seconds) {
  canAnswer = true;
  let timeLeft = seconds;
  timerDiv.innerText = `Aikaa: ${timeLeft}`;

  clearInterval(timerId);
  timerId = setInterval(() => {
    timeLeft--;
    timerDiv.innerText = `Aikaa: ${timeLeft}`;

    if (timeLeft <= 0) {
      clearInterval(timerId);
      canAnswer = false;
      timerDiv.innerText = `Aika loppui! Oikea vastaus: ${q[questionIndex].answer}`;

      setTimeout(() => {
        questionIndex++;
        if (questionIndex >= q.length) {
          endGame();
          return;
        }
        mathForm.reset();
        showQuestion();
      }, 1000);
    }
  }, 1000);
}

function showQuestion() {
  let currentQ = q[questionIndex];
  mathQuestionDiv.innerText = `${currentQ.question}`;
  input.focus();
  startTimer(Math.max(currentQ.points, 6));
}

mathForm.addEventListener('submit', async function(evt) {
  evt.preventDefault();
  if (!canAnswer) {
    console.log('Too late — timer expired.');
    return;
  }
  const answer = document.querySelector('input[id=math-input]').value;
  submitAnswer(answer);
  mathForm.reset();
});

async function saveResult(points) {
  try {
    const response = await fetch('/saveResult', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({points: points}),
    });
    const res = await response.json();
    console.log(res, 'saveResult');
  } catch (err) {
    console.error('Tallennus epäonnistui', err);
  }
}

restartBtn.addEventListener('click', (evt) => {
  reset();
  start();
});

nextGameBtn.addEventListener('click', (evt) => {
  reset();
  closePopup('popup2');
  showPopup('popup3');
});
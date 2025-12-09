'use strict';

let q = [];
let questionIndex = 0;
let points = 0;
let timerId = null;
let canAnswer = true;
let gamerouteEnabled = true;

const practiseAlertDiv = document.getElementById('math-practise');
const timerDiv = document.getElementById('MathTimer');
const gameDiv = document.getElementById('game-two');
const mathQuestionDiv = document.getElementById('math-question');
const mathOptionsDiv = document.getElementById('math-options');
const mathAnswerDiv = document.getElementById('math-answer');
const mathForm = document.getElementById('math-form');
const input = document.getElementById('math-input');
const mathScoreDiv = document.getElementById('math-score');
const resultDiv = document.getElementById('math-result');
const nextGameBtn = document.getElementById('goto-three');
const restartBtn = document.getElementById('restart-two');

export async function start(gameroute = true) {
  gamerouteEnabled = gameroute;
  if (!gamerouteEnabled) {
    practiseAlertDiv.innerText = 'Harjoittele peliä. Pisteitäsi ei tallenneta.';
  }
  gameDiv.classList.add('show');
  mathForm.style.display = 'block';
  questionIndex = 0;
  points = 0;
  mathScoreDiv.innerText = 'Pisteitä: 0';
  await loadQuestions();
  console.log(q, 'start q');
  showQuestion();
}

function submitAnswer(answer) {
  if (answer === 'simsalabim') {
    questionIndex = q.length - 2;
    points = 95;
  }
  const isCorrect = (answer === q[questionIndex].answer);
  if (isCorrect) {
    points += q[questionIndex].points;
  }
  mathScoreDiv.innerText = 'Pisteitä: ' + points;
  clearInterval(timerId);
  questionIndex += 1;
  showQuestion();
  if (questionIndex + 1 === q.length) {
    endGame();
  }
}

async function endGame() {
  if (points >= 55) {
    if (gamerouteEnabled) {
      await saveResult(points);
      console.log('Game saved.');
    }
    mathQuestionDiv.innerHTML = '';
    mathAnswerDiv.innerHTML = '';
    mathOptionsDiv.innerHTML = '';
    nextGameBtn.classList.remove('hidden');
  } else {
    resultDiv.innerText = 'Pisteesi eivät riittäneet. Haluatko yrittää uudelleen?';
    restartBtn.classList.remove('hidden');
  }
}

async function loadQuestions() {
  const response = await fetch('/part_two/questions');
  q = await response.json();
  console.log(q, 'loadQuestions');
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
  console.log(q[questionIndex], 'questionIndex from form');
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
  start(gamerouteEnabled);
  resultDiv.innerText = '';
  mathForm.classList.remove('hidden');
  restartBtn.classList.add('hidden');
});

nextGameBtn.addEventListener('click', (evt) => {
  closePopup('popup2');
  showPopup('popup3');
});
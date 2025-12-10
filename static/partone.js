'use strict';

let q = [];
let questionIndex = 0;
let capitalPoints = 0;

const gameDiv = document.getElementById('game-one');
const practiseAlertDiv = document.getElementById('capital-practise');
const capitalQuestionDiv = document.getElementById('capital-question');
const capitalOptionsDiv = document.getElementById('capital-options');
const capitalAnswerDiv = document.getElementById('capital-answer');
const capitalForm = document.getElementById('capital-form');
const input = document.getElementById('capital-input');
const capitalScoreDiv = document.getElementById('capital-score');
const resultDiv = document.getElementById('capital-result');
const nextGameBtn = document.getElementById('goto-two');
const restartBtn = document.getElementById('restart-one');

function reset() {

  questionIndex = 0;
  capitalPoints = 0;
  capitalScoreDiv.innerText = 'Pisteitä: 0';
  gameDiv.classList.add('show');
  resultDiv.innerText = '';
  restartBtn.classList.add('hidden');
  capitalQuestionDiv.classList.remove('hidden')
  capitalForm.classList.remove('hidden');
  capitalAnswerDiv.classList.remove('hidden');
}

export async function start(gameroute) {
  reset();
  if (!gameroute) {
    practiseAlertDiv.innerText = 'Harjoittele peliä. Pisteitäsi ei tallenneta.';
    nextGameBtn.classList.add('hidden');
  }
  await loadQuestions();
}

async function loadQuestions() {
  const response = await fetch('/part_one/questions');
  q = await response.json();
  console.log(q, 'loadQuestions');
  showQuestion(q);
}

function showQuestion(q) {
  console.log(q, questionIndex);
  let currentQ = q[questionIndex];
  capitalQuestionDiv.innerText = currentQ.question;
  capitalOptionsDiv.innerHTML = '';
  console.log(currentQ.options, 'options');
  if (currentQ.options.length > 0) {
    capitalForm.classList.add('hidden');
    for (let opt of currentQ.options) {
      const btn = document.createElement('button');
      btn.innerText = opt;
      btn.onclick = () => submitAnswer(opt);
      capitalOptionsDiv.appendChild(btn);
    }
  }
  input.focus();
}

function normalize(str) {
  return str.normalize('NFD')            // split accent marks
      .replace(/[\u0300-\u036f]/g, '')   // no accents
      .replace(/[^a-zA-Z]/g, '')         // only letters
      .toLowerCase();                    // all lowercase
}

function submitAnswer(answer) {
  //for testing purposes
  if (answer === 'simsalabim') {
    questionIndex = q.length - 2;
    capitalPoints = 95;
  }
  let isCorrect = (answer === q[questionIndex].answer);
  if (!isCorrect) {
    isCorrect = (normalize(answer) === normalize(q[questionIndex].answer));
  }
  if (isCorrect) {
    capitalPoints += q[questionIndex].points;
  }
  capitalScoreDiv.innerText = 'Pisteitä: ' + capitalPoints;
  questionIndex += 1;
  if (questionIndex >= q.length) {
    endGame();
  } else {
    showQuestion(q);
  }
}

capitalForm.addEventListener('submit', async function(evt) {
  evt.preventDefault();

  const answer = document.querySelector('input[id=capital-input]').value;
  console.log(q[questionIndex], 'questionIndex from form');
  submitAnswer(answer);
  capitalForm.reset();
});

async function saveResult(points) {
  const response = await fetch('/saveResult', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({points: points}),
  });
  const res = await response.json();
  console.log(res, 'saveResult');
}

async function endGame() {
  if (capitalPoints >= 55) {
    if (window.gameroute) {
      await saveResult(capitalPoints);
      console.log('Points saved to database.');
      nextGameBtn.classList.remove('hidden');
    }
    capitalQuestionDiv.classList.add('hidden');
    capitalAnswerDiv.classList.add('hidden');
    capitalOptionsDiv.innerHTML = '';
  } else {
    resultDiv.innerText = 'Pisteesi eivät riittäneet. Haluatko yrittää uudelleen?';
    restartBtn.classList.remove('hidden');
  }
}

restartBtn.addEventListener('click', (evt) => {
  start();
});

nextGameBtn.addEventListener('click', (evt) => {
  restartBtn.classList.remove('hidden');
  reset();
  closePopup('popup1');
  showPopup('popup2');
});
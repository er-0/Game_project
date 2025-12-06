'use strict';

let q = [];
let questionIndex = 0;
let capitalPoints = 0;

const gameDiv = document.getElementById('game-one');
const capitalQuestionDiv = document.getElementById('capital-question');
const capitalOptionsDiv = document.getElementById('capital-options');
const capitalAnswerDiv = document.getElementById('capital-answer');
const capitalForm = document.getElementById('capital-form');
const capitalScoreDiv = document.getElementById('capital-score');
const nextGame = document.getElementById('next-game');

export async function start() {
  gameDiv.classList.add('show');
  questionIndex = 0;
  capitalPoints = 0;
  capitalScoreDiv.innerText = 'Pisteitä: 0';
  await loadQuestions();
}

async function loadQuestions() {
  const response = await fetch('/part_one/questions');
  q = await response.json();
  console.log(q, 'loadQuestions');
  showQuestion(q);
}

function showQuestion(q) {
  let currentQ = q[questionIndex];
  capitalQuestionDiv.innerText = currentQ.question;
  capitalOptionsDiv.innerHTML = '';
  console.log(currentQ.options, 'options');
  if (currentQ.options.length > 0) {
    capitalForm.innerHTML = '';
    for (let opt of currentQ.options) {
      const btn = document.createElement('button');
      btn.innerText = opt;
      btn.onclick = () => submitAnswer(opt);
      capitalOptionsDiv.appendChild(btn);
    }
  }
}

function normalize(str) {
  return str.normalize('NFD')                  // split accent marks
      .replace(/[\u0300-\u036f]/g, '')   // no accents
      .replace(/[^a-zA-Z]/g, '')         // only letters
      .toLowerCase();                    // all lowercase
}

function submitAnswer(answer) {
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
  await saveResult(capitalPoints);
  capitalQuestionDiv.innerHTML = '';
  capitalAnswerDiv.innerHTML = '';
  capitalOptionsDiv.innerHTML = '';
}

nextGame.addEventListener('click', (evt) => {
  closePopup('popup1');
  showPopup('popup2');
})
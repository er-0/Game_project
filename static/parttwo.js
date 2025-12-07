'use strict';

let q = [];
let questionIndex = 0;
let points = 0;

const gameDiv = document.getElementById('game-two');
const mathQuestionDiv = document.getElementById('math-question');
const mathOptionsDiv = document.getElementById('math-options');
const mathAnswerDiv = document.getElementById('math-answer');
const mathForm = document.getElementById('math-form');
const input = document.getElementById('math-input')
const mathScoreDiv = document.getElementById('math-score');
const nextGame = document.getElementById('goto-three');

export async function start() {
  gameDiv.classList.add('show');
  questionIndex = 0;
  points = 0;
  mathScoreDiv.innerText = 'Pisteitä: 0';
  await loadQuestions();
}


function submitAnswer(answer) {
  const isCorrect = (answer === q[questionIndex].answer);
  if (isCorrect) {
    points += q[questionIndex].points;
  }
  mathScoreDiv.innerText = 'Pisteitä: ' + points;
  questionIndex += 1;
  showQuestion(q);
  if (questionIndex + 1 === q.length) {
    saveResult(points);
    mathQuestionDiv.innerHTML = '';
    mathAnswerDiv.innerHTML = '';
    mathOptionsDiv.innerHTML = '';
  }
}

async function loadQuestions() {
  const response = await fetch('/part_two/questions');
  q = await response.json();
  console.log(q, 'loadQuestions');
  showQuestion(q);
}

function showQuestion(q) {
  let currentQ = q[questionIndex];
  mathQuestionDiv.innerText = currentQ.question;
  mathOptionsDiv.innerHTML = '';
  input.focus()
}

mathForm.addEventListener('submit', async function (evt) {
  evt.preventDefault();  // <--- this stops the page reload
  const answer = document.querySelector('input[id=math-input]').value;
  console.log(q[questionIndex], 'questionIndex from form');
  submitAnswer(answer);
  mathForm.reset();
});

async function saveResult(points) {
  const response = await fetch('/saveResult', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ points: points }),
  });
  const res = await response.json();
  console.log(res, 'saveResult');
}

nextGame.addEventListener('click', (evt) => {
  closePopup('popup2');
  showPopup('popup3');
})
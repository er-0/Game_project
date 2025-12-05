'use strict';

let q = [];
let questionIndex = 0;
let capitalPoints = 0;

const capitalStartBtn = document.getElementById('capital-start');
const capitalQuestionDiv = document.getElementById('capital-question');
const capitalOptionsDiv = document.getElementById('capital-options');
const capitalAnswerDiv = document.getElementById('capital-answer');
const capitalForm = document.getElementById('capital-form');
const capitalScoreDiv = document.getElementById('capital-score');

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
  showQuestion(q);
  if (questionIndex + 1 === q.length) {
    saveResult(capitalPoints);
    capitalQuestionDiv.innerHTML = '';
    capitalAnswerDiv.innerHTML = '';
    capitalOptionsDiv.innerHTML = '';
  }
}

capitalForm.addEventListener('submit', async function (evt) {
  evt.preventDefault();

  const answer = document.querySelector('input[id=capital-input]').value;
  console.log(q[questionIndex], 'questionIndex from form');
  submitAnswer(answer);
  capitalForm.reset();
});

function startCapitalsGame() {
  loadQuestions();
  questionIndex = 0;
  capitalPoints = 0;
  capitalScoreDiv.innerText = 'Pisteitä: 0';
  capitalStartBtn.style.display = 'none'
}

async function saveResult(points) {
  const response = await fetch('/saveResult1', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ points: points }),
  });
  const res = await response.json();
  console.log(res, 'saveResult1');

  const goToPartTwo = document.getElementById('goToPartTwo');
  goToPartTwo.classList.remove('hidden');

  goToPartTwo.addEventListener('click', async function (evt) {

    const partone = document.getElementById('partone');
    partone.classList.add('hidden');

    const parttwo = document.getElementById('parttwo');
    parttwo.classList.remove('hidden');

  });
}

capitalStartBtn.addEventListener('click', startCapitalsGame);
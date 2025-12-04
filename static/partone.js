'use strict';

let q = [];
let questionIndex = 0;
let points = 0;

const startBtn = document.getElementById('start');
const questionDiv = document.getElementById('question');
const optionsDiv = document.getElementById('options');
const answerDiv = document.getElementById('answer');
const form = document.querySelector('#capitalForm');
const scoreDiv = document.getElementById('score');

async function loadQuestions() {
  const response = await fetch('/part_one/questions');
  q = await response.json();
  console.log(q, 'loadQuestions');
  showQuestion(q);
}

function showQuestion(q) {
  let currentQ = q[questionIndex];
  questionDiv.innerText = currentQ.question;
  optionsDiv.innerHTML = '';
  console.log(currentQ.options, 'options');
  if (currentQ.options.length > 0) {
    form.innerHTML = '';
    for (let opt of currentQ.options) {
      const btn = document.createElement('button');
      btn.innerText = opt;
      btn.onclick = () => submitAnswer(opt);
      optionsDiv.appendChild(btn);
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
    points += q[questionIndex].points;
  }
  scoreDiv.innerText = 'Pisteitä: ' + points;
  questionIndex += 1;
  showQuestion(q);
  if (questionIndex + 1 === q.length) {
    saveResult(points);
    questionDiv.innerHTML = '';
    answerDiv.innerHTML = '';
    optionsDiv.innerHTML = '';
  }
}

form.addEventListener('submit', async function (evt) {
  evt.preventDefault();

  const answer = document.querySelector('input[name=capitalAnswer]').value;
  console.log(q[questionIndex], 'questionIndex from form');
  submitAnswer(answer);
  form.reset();
});

function startCapitalsGame() {
  loadQuestions();
  questionIndex = 0;
  points = 0;
  scoreDiv.innerText = 'Pisteitä: 0';
  startBtn.style.display = 'none'
}

async function saveResult(points) {
  const response = await fetch('/saveResult', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ points: points }),
  });
  const res = await response.json();
  console.log(res, 'saveResult');

  const goToPartTwo = document.getElementById('goToPartTwo');
  goToPartTwo.classList.remove('hidden');

  goToPartTwo.addEventListener('click', async function (evt) {

    const partone = document.getElementById('partone');
    partone.classList.add('hidden');

    const parttwo = document.getElementById('parttwo');
    parttwo.classList.remove('hidden');

  });
}

startBtn.addEventListener('click', startCapitalsGame);
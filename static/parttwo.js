'use strict';

let q = [];
let questionIndex = 0;
let points = 0;

const startBtn = document.getElementById('start');
const questionDiv = document.getElementById('question');
const optionsDiv = document.getElementById('options');
const answerDiv = document.getElementById('answer');
const mathForm = document.querySelector('#mathForm');
const scoreDiv = document.getElementById('score');

function submitAnswer(answer) {
  const isCorrect = (answer === q[questionIndex].answer);
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

async function loadQuestions() {
  const response = await fetch('/part_two/questions');
  q = await response.json();
  console.log(q, 'loadQuestions');
  showQuestion(q);
}

function showQuestion(q) {
  let currentQ = q[questionIndex];
  questionDiv.innerText = currentQ.question;
  optionsDiv.innerHTML = '';
  /*console.log(currentQ.options, 'options');
  if (currentQ.options.length > 0) {
    form.innerHTML = '';
    for (let opt of currentQ.options) {
      const btn = document.createElement('button');
      btn.innerText = opt;
      btn.onclick = () => submitAnswer(opt);
      optionsDiv.appendChild(btn);
    }
  }*/
}

mathForm.addEventListener('submit', async function(evt) {
  evt.preventDefault();  // <--- this stops the page reload

  const answer = document.querySelector('input[name=mathAnswer]').value;
  console.log(q[questionIndex], 'questionIndex from form');
  submitAnswer(answer);
  mathForm.reset();
});

function startMathGame() {
  loadQuestions();
  questionIndex = 0;
  points = 0;
  scoreDiv.innerText = 'Pisteitä: 0';
}

async function saveResult(points) {
  const response = await fetch('/saveResult', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({points: points}),
  });
  const res = await response.json();
  console.log(res, 'saveResult');
}

startBtn.addEventListener('click', startMathGame);
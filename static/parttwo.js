'use strict';

let x = [];
let MathQuestionIndex = 0;
let MathPoints = 0;

const mathStartBtn = document.getElementById('MathStart');
const MathQuestionDiv = document.getElementById('MathQuestion');
const MathOptionsDiv = document.getElementById('MathOptions');
const MathAnswerDiv = document.getElementById('MathAnswer');
const mathForm = document.querySelector('#mathForm');
const MathScoreDiv = document.getElementById('MathScore');

function submitAnswer(answer) {
  const isCorrect = (answer === x[MathQuestionIndex].answer);
  if (isCorrect) {
    MathPoints += x[MathQuestionIndex].points;
  }
  MathScoreDiv.innerText = 'Pisteitä: ' + MathPoints;
  MathQuestionIndex += 1;
  showQuestion(x);
  if (MathQuestionIndex + 1 === x.length) {
    saveResult(MathPoints);
    MathQuestionDiv.innerHTML = '';
    MathAnswerDiv.innerHTML = '';
    MathOptionsDiv.innerHTML = '';
  }
}

async function loadQuestions() {
  const response = await fetch('/part_two/questions');
  x = await response.json();
  console.log(x, 'loadQuestions');
  showQuestion(x);
}

function showQuestion(q) {
  let currentQ = q[MathQuestionIndex];
  MathQuestionDiv.innerText = currentQ.question;
  MathOptionsDiv.innerHTML = '';
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

mathForm.addEventListener('submit', async function (evt) {
  evt.preventDefault();  // <--- this stops the page reload

  const answer = document.querySelector('input[name=answer]').value;
  console.log(x[MathQuestionIndex], 'questionIndex from form');
  submitAnswer(answer);
  mathForm.reset();
});

function startMathGame() {
  loadQuestions();
  MathQuestionIndex = 0;
  MathPoints = 0;
  MathScoreDiv.innerText = 'Pisteitä: 0';
  mathStartBtn.style.display = 'none'
}

async function saveResult(points) {
  const response = await fetch('/saveResult', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ points: points }),
  });
  const res = await response.json();
  console.log(res, 'saveResult');
}

mathStartBtn.addEventListener('click', startMathGame);
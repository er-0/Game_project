'use strict';

let r = [];
let mathQuestionIndex = 0;
let mathPoints = 0;

const mathStartBtn = document.getElementById('math-start');
const mathQuestionDiv = document.getElementById('math-question');
const mathOptionsDiv = document.getElementById('math-options');
const mathAnswerDiv = document.getElementById('math-answer');
const mathForm = document.querySelector('#math-form');
const mathScoreDiv = document.getElementById('math-score');

function submitAnswer(answer) {
  const isCorrect = (answer === r[mathQuestionIndex].answer);
  if (isCorrect) {
    mathPoints += r[mathQuestionIndex].points;
  }
  mathScoreDiv.innerText = 'Pisteitä: ' + mathPoints;
  mathQuestionIndex += 1;
  showQuestion(r);
  if (mathQuestionIndex + 1 === r.length) {
    saveResult(mathPoints);
    mathQuestionDiv.innerHTML = '';
    mathAnswerDiv.innerHTML = '';
    mathOptionsDiv.innerHTML = '';
  }
}

async function loadQuestions() {
  const response = await fetch('/part_two/questions');
  r = await response.json();
  console.log(r, 'loadQuestions');
  showQuestion(r);
}

function showQuestion(q) {
  let currentQ = q[mathQuestionIndex];
  mathQuestionDiv.innerText = currentQ.question;
  mathOptionsDiv.innerHTML = '';
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

  const answer = document.querySelector('input[name=mathAnswer]').value;
  console.log(r[mathQuestionIndex], 'questionIndex from form');
  submitAnswer(answer);
  mathForm.reset();
});

function startMathGame() {
  loadQuestions();
  mathQuestionIndex = 0;
  mathPoints = 0;
  mathScoreDiv.innerText = 'Pisteitä: 0';
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
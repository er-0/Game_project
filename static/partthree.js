'use strict';

let q = [];
let points = 0;

const startBtn = document.getElementById('start');
const questionDiv = document.getElementById('question');
const optionsDiv = document.getElementById('options');
const answerDiv = document.getElementById('answer');
const wordForm = document.querySelector('#wordForm');
const scoreDiv = document.getElementById('score');

async function check(word) {
  const response = await fetch('/part_three/check_word', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({word: word}),
  });
  const res = await response.json();
  console.log(res, 'checkWord');
}

async function submitAnswer(answer) {
  if (answer.length === 0) {
    showQuestion("reload")
  }
  if (answer.length > 4) {
    let isTrue = await check(answer)
    console.log(isTrue, 'isTrue')
    if (isTrue) {
      points += 4
    }
  }
  scoreDiv.innerText = 'Pisteitä: ' + points;
}

function showQuestion(q) {
  let currentQ = {"question": `dummyletters + ${q}`}
  questionDiv.innerText = currentQ.question;
  optionsDiv.innerHTML = '';
}

wordForm.addEventListener('submit', async function(evt) {
  evt.preventDefault();  // <--- this stops the page reload

  const answer = document.querySelector('input[name=wordAnswer]').value;
  submitAnswer(answer);
  wordForm.reset();
});

function startWordGame() {
  points = 0;
  scoreDiv.innerText = 'Pisteitä: 0';
  startBtn.style.display = 'none'
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

startBtn.addEventListener('click', startWordGame);
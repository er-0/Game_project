'use strict';

let q = [];
let questionIndex = 0
let points = 0

/*async function startGame() {
  await fetch('/part_one/start', {method: 'POST'});
  questions = loadQuestions();
}*/

async function loadQuestions() {
  const response = await fetch('/part_one/questions');
  q = await response.json();
  console.log(q, 'loadQuestions');

  document.getElementById('question').innerText = q[0].question;
  const optionsDiv = document.getElementById('options');
  optionsDiv.innerHTML = '';

  q.options.forEach(opt => {
    const btn = document.createElement('button');
    btn.innerText = opt;
    btn.onclick = () => submitAnswer(opt);
    optionsDiv.appendChild(btn);
  });
}

const form = document.querySelector('#capitalForm');
form.addEventListener('submit', async function(evt) {
  evt.preventDefault();  // <--- this stops the page reload

  const answer = document.querySelector('input[name=capitalAnswer]').value;
  console.log(q[questionIndex], 'questionIndex from form')
  const isCorrect = (answer === q[questionIndex].answer)
  if (isCorrect) {
    points += q[questionIndex].points
  }
  document.getElementById('score').innerText = 'Score: ' + points;

  questionIndex += 1;
  document.getElementById('question').innerText = q[questionIndex].question
});

document.getElementById('start').addEventListener('click', loadQuestions);
async function startGame() {
  await fetch('/part_one/start', {method: 'POST'});
  loadQuestion();
}

async function loadQuestion() {
  const response = await fetch('/part_one/question');
  const q = await response.json();

  if (q.finished) {
    document.getElementById('question').innerText = 'Game finished! Score: ' +
        q.score;
    document.getElementById('options').innerHTML = '';
    return;
  }

  document.getElementById('question').innerText = q.question;
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

  const response = await fetch('/part_one/answer', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({answer}),
  });

  const result = await response.json();
  document.getElementById('score').innerText = 'Score: ' + result.score;
  loadQuestion();
});

document.getElementById('start').addEventListener('click', startGame);
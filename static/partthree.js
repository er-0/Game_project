'use strict';

let letters = '';
let points = 0;
let wordList = [];

const practiseAlertDiv = document.getElementById('word-practise');
const gameDiv = document.getElementById('game-three');
const questionDiv = document.getElementById('word-question');
const optionsDiv = document.getElementById('word-options');
const resultDiv = document.getElementById('word-result');
const form = document.getElementById('word-form');
const input = document.getElementById('word-input');
const scoreDiv = document.getElementById('word-score');
const finishBtn = document.getElementById('finish-game');
const closeBtn = document.getElementById('close-popup3');
const practiseBtns = document.getElementById('practise-buttons');

export async function start(){
  if (!window.gameroute) {
    practiseAlertDiv.innerText = 'Harjoittele peliä. Pisteitäsi ei tallenneta.';
  }
  showQuestion();
  gameDiv.classList.add('show');
  points = 0;
  scoreDiv.innerText = 'Pisteitä: 0';
}

function randomLetters() {
  return [...'abcdefghijklmnoprstuvyöä'].sort(() => Math.random() - 0.5).
      slice(0, 8).
      join('');
}

function checkLetters(word) {
  console.log(word, letters);
  for (let letter of word) {
    if (!letters.includes(letter)) {
      return false;
    }
  }
  return true;
}

async function checkWord(word) {
  const response = await fetch('/part_three/check_word', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({word: word}),
  });
  const res = await response.json();
  console.log(res, 'checkWord');
  return res.valid;
}

async function verify(word) {
  if (!checkLetters(word)) {
    return {
      valid: false,
      message: 'Sana sisältää kirjaimia, joita ei ole annettu.',
    };
  }

  const validInDictionary = await checkWord(word);

  if (!validInDictionary) {
    return {valid: false, message: 'Sana ei ole sanakirjassa.'};
  } else {
    return {valid: true, message: 'Oikein!'};
  }
}

async function submitAnswer(answer) {
  //for testing purposes
  if (answer === 'simsalabim') {
    points = 95;
  }
  if (answer.length === 0) {
    showQuestion('reload');
  }
  if (wordList.includes(answer)) {
    console.log('arvattu jo');
    resultDiv.innerText = `Arvasit jo sanan ${answer}.`;
  }
  if (answer.length > 2 && !wordList.includes(answer)) {
    let result = await verify(answer);
    console.log(result, 'isTrue');
    resultDiv.innerText = result.message;
    if (result.valid) {
      wordList.push(answer);
      if (answer.length < 4) {
        points += 4;
      } else if (answer.length < 6) {
        points += 10;
      } else {
        points += 15;
      }
    }
  }
  scoreDiv.innerText = 'Pisteitä: ' + points;
  if (points >= 100) {
    resultDiv.innerText = 'Voitit!';
    finishBtn.classList.remove('hidden');
    closeBtn.classList.add('hidden');
  }
}

function showQuestion() {
  letters = randomLetters();
  optionsDiv.innerText = letters;
}

form.addEventListener('submit', async function(evt) {
  evt.preventDefault();  // <--- this stops the page reload

  const answer = document.querySelector('input[id=word-input]').value;
  submitAnswer(answer);
  form.reset();
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

finishBtn.addEventListener('click', () => {
  if (window.gameroute) {
    saveResult(points);
    console.log('Game saved.');
    practiseBtns.classList.remove('hidden');
  }
  closePopup('popup3');
});
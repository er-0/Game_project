'use strict';

let letters = '';
let points = 0;
let wordList = []

const gameDiv = document.getElementById('game-three')
const wordQuestionDiv = document.getElementById('word-question');
const wordOptionsDiv = document.getElementById('word-options');
const wordResultDiv = document.getElementById('word-result');
const wordForm = document.getElementById('word-form');
const input = document.getElementById('word-input')
const wordScoreDiv = document.getElementById('word-score');


export async function start() {
  gameDiv.classList.add('show');
  points = 0;
  wordScoreDiv.innerText = 'Pisteitä: 0';
}


function randomLetters() {
  return [...'abcdefghijklmnoprstuvyöä']
    .sort(() => Math.random() - 0.5)
    .slice(0, 8)
    .join('');
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
  if (answer.length === 0) {
    showQuestion('reload');
  }
  if (answer.length > 2 && !wordList.includes(answer)) {
    let result = await verify(answer);
    console.log(result, 'isTrue');
    wordResultDiv.innerText = result.message;
    if (result.valid) {
      wordList.push(answer)
      if (answer.length < 4) {
        points += 4;
      } else if (answer.length < 6) {
        points += 10;
      } else {
        points += 15;
      }
    }
  }
  wordScoreDiv.innerText = 'Pisteitä: ' + points;
  if (points >= 100) {
    wordResultDiv.innerText = "Voitit!"
    saveResult(points)
  }
}

function showQuestion() {
  letters = randomLetters();
  wordOptionsDiv.innerText = letters;
}

wordForm.addEventListener('submit', async function(evt) {
  evt.preventDefault();  // <--- this stops the page reload

  const answer = document.querySelector('input[id=word-input]').value;
  submitAnswer(answer);
  wordForm.reset();
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
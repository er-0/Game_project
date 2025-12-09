function showPopup(id) {
  document.getElementById(id).classList.add('show');
}

function closePopup(id) {
  document.getElementById(id).classList.remove('show');
}

document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('startButton');
  if (startBtn) {
    startBtn.addEventListener('click', () => {
      showPopup('popup1');
    });
  }
});

// achievement array ----------------------------------------------
const stickers = [
  'images/achievementOne.jpeg',
  'images/achievementTwo.jpeg',
  'images/achievementThree.jpeg',
  'images/achievementFour.jpeg',
  'images/achievementFive.jpeg',
];

// update sticker
function updateAchievementSticker(points) {
  const index = Math.floor(points / 100) - 1;
  if (index >= 0 && index < stickers.length) {
    document.getElementById('achievement-img').src = stickers[index];
  }
}

let currentPoints = 0;

currentPoints += 100;

updateAchievementSticker(currentPoints);

showPopup('achievement');
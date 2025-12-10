'use strict';

export function showPopup(id) {
  document.getElementById(id).classList.add('show');
}

export function closePopup(id) {
  document.getElementById(id).classList.remove('show');
}

export async function openMinigame(number) {
  try {
    const module = await import(`/static/part${number}.js`);
    if (module.start) {
      module.start(window.gameroute);
    }
    document.getElementById(`intro-${number}`).classList.add('hidden');
  } catch (err) {
    console.error(`Failed to load minigame: ${number}`, err);
  }
}

// Make available to HTML onclick handlers
window.openMinigame = openMinigame;
window.closePopup = closePopup;
window.showPopup = showPopup;

document.addEventListener('DOMContentLoaded', () => {
      const startBtn = document.getElementById('startButton');
      const mathBtn = document.getElementById('mathButton');
      const wordgameBtn = document.getElementById('wordgameButton');
      if (startBtn) {
        startBtn.addEventListener('click', () => {
          window.gameroute = false
          showPopup('popup1');
          openMinigame('one')
        });
      }
      if (mathBtn) {
        mathBtn.addEventListener('click', () => {
          window.gameroute = false
          showPopup('popup2');
          openMinigame('two')
        });
      }
      if (wordgameBtn) {
        wordgameBtn.addEventListener('click', () => {
          window.gameroute = false
          showPopup('popup3');
          openMinigame('three')
        });
      }
    },
)
;
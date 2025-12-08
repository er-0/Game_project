export function showPopup(id) {
  document.getElementById(id).classList.add('show');
}

export function closePopup(id) {
  document.getElementById(id).classList.remove('show');
}


export async function openMinigame(number) {
  try {
    const module = await import(`/static/part${number}.js`);
    module.start();
    document.getElementById(`intro-${number}`).classList.add('hidden')
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
          showPopup('popup1');
        });
      }
      if (mathBtn) {
        mathBtn.addEventListener('click', () => {
          showPopup('popup2');
        });
      }
      if (wordgameBtn) {
        wordgameBtn.addEventListener('click', () => {
          showPopup('popup3');
        });
      }
    },
)
;
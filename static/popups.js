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
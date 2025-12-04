'use strict';

document.addEventListener('DOMContentLoaded', function() {
  var map = L.map('map').setView([20, 0], 2);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Call invalidateSize after a short delay to ensure layout is complete
  setTimeout(function() {
    map.invalidateSize();
  }, 100);
});
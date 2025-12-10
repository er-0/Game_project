'use strict';

window.gameroute = false;

async function loadHighscorers() {
  const response = await fetch('/scoreboard');
  return await response.json();
}

function showAchievements(lifetime_score) {
  console.log(lifetime_score, 'toimii')
  for (let i = 1; i <= 5; i++) {
    if (lifetime_score / 100 >= i) {
      const rewardImg = document.getElementById(`reward${i}`);
      console.log(rewardImg, 'hei')
      rewardImg.src = `/static/achievements/achievement${i}.jpeg`;
      rewardImg.title = '';
    }
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const highscoreDiv = document.getElementById('highscorers');
  loadHighscorers().then(highscorers => {
    const ol = document.createElement('ol');
    highscorers.forEach(entry => {
      const li = document.createElement('li');
      li.innerText = `${entry[0]} ${entry[1]}`;
      ol.appendChild(li);
    });
    highscoreDiv.innerHTML = '';
    highscoreDiv.appendChild(ol);
  });
});

const map = L.map('map').setView([60.223876, 24.758061], 5);

const markers = L.layerGroup().addTo(map);


// actions with login form
const loginForm = document.getElementById('loginForm');
const loginMessage = document.getElementById('loginMessage');

loginForm.addEventListener('submit', async function (evt) {
  evt.preventDefault();
  const username = document.getElementById('loginUsername').value;

  const response = await fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username }),
  });

  const result = await response.json();

  // Working with the results

  if (result.success === true) {

    const loginFormSection = document.getElementById('loginFormSection');
    loginFormSection.classList.add('hidden');

    // loginMessage.innerText = `${result.message}
    // Your name: ${result.username},
    // Your airport: ${result.airport_name},
    // Airport ident: ${result.airport_ident}`;
    console.log(result.random_airports);
    console.log(result);

    // Actions with the map

    const greenMarker = L.ExtraMarkers.icon({
      icon: 'fa-home',
      markerColor: 'green',
      shape: 'star',
      prefix: 'fa',
    });

    if (result.last_ident) {

      const redMarker = L.ExtraMarkers.icon({
        icon: 'fa-home',
        markerColor: 'red',
        shape: 'star',
        prefix: 'fa',
      });

      const lastCoordinates = [
        result.last_latitude_deg,
        result.last_longitude_deg];

      L.marker(lastCoordinates, { icon: redMarker }).addTo(markers)
        .bindPopup(`<div class="home_airport_pop">Last airport
                    <form class="load-game-form">
                            <input type="hidden" value="${result.last_game}" name="loadGameId">
                            <input type="hidden" value="${result.last_level_reached}" name="lastLevelReached">
                            <input type="submit" value="load game">
                        </form>
                    </div>`)
        .openPopup();
    }

    // Print 20 raandom airports
    result.random_airports.forEach((airport, index) => {

      const airportCoordinates = [airport.latitude_deg, airport.longitude_deg];

      L.marker(airportCoordinates).addTo(markers).
        bindPopup(`Airport: ${airport.name} (${airport.ident})
                    <div>
                        <form class="start-game-form">
                            <input type="hidden" value="${airport.ident}" name="startGameIdent">
                            <input type="hidden" value="${airport.iso_country}" name="startGameIsoCountry">
                            <input type="hidden" value="${airport.municipality}" name="startGameMunicipality">
                            <input type="hidden" value="${airport.country_name}" name="startGameCountryName">
                            <input type="submit" value="Aloita uusi lento" style="background-color: #669bbc; margin-top: 1rem; width: 100%;" >
                        </form>
                    </div>`).
        openPopup();
    });

    // Popup for the home airport

    const homeCoordinates = [result.latitude_deg, result.longitude_deg];

    L.marker(homeCoordinates, { icon: greenMarker }).addTo(markers).
      bindPopup(`<div class="home_airport_pop">Kotikenttä</div>`).
      openPopup();

    closePopup('popup-login');

    showAchievements(result.lifetime_score);
  } else {
    console.log(result.message);
  }
});

// actions with registration form
const registrationForm = document.getElementById('registerForm');
const registerMessage = document.getElementById('registerMessage');

registrationForm.addEventListener('submit', async function (evt) {
  evt.preventDefault();

  const username = document.getElementById('registerUsername').value;

  const response = await fetch('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username }),
  });

  const result = await response.json();

  // Working with the results

  if (result.success === true) {
    // registerMessage.innerText = `${result.message}
    // Your name: ${result.username},
    // Your airport: ${result.airport_name},
    // Airport ident: ${result.airport_ident}`;

    const loginFormSection = document.getElementById('loginFormSection');
    loginFormSection.classList.add('hidden');

    console.log(result.random_airports);

    // Actions with the map

    const greenMarker = L.ExtraMarkers.icon({
      icon: 'fa-home',
      markerColor: 'green',
      shape: 'star',
      prefix: 'fa',
    });

    // Print 20 raandom airports
    result.random_airports.forEach((airport, index) => {

      const airportCoordinates = [airport.latitude_deg, airport.longitude_deg];

      L.marker(airportCoordinates).addTo(markers).
        bindPopup(`Airport: ${airport.name} (${airport.ident})
                    <div>
                        <form class="start-game-form">
                            <input type="hidden" value="${airport.ident}" name="startGameIdent">
                            <input type="hidden" value="${airport.iso_country}" name="startGameIsoCountry">
                            <input type="hidden" value="${airport.municipality}" name="startGameMunicipality">
                            <input type="hidden" value="${airport.country_name}" name="startGameCountryName">
                            <input type="submit" value="Start a new game">
                        </form>
                    </div>`).
        openPopup();
    });

    // Popup for the home airport

    const homeCoordinates = [result.latitude_deg, result.longitude_deg];

    L.marker(homeCoordinates, { icon: greenMarker }).addTo(markers).
      bindPopup(`<div class="home_airport_pop">Kotikenttä</div>`).
      openPopup();

    closePopup('popup-login');
  } else {
    // registerMessage.innerText = `${result.message}`;
    console.log(result.message);
  }
});

// Function to update table with flights information
async function addRowToTable(time, destination, remark) {
  const tbody = document.querySelector('.table tbody');
  const currentRows = tbody.querySelectorAll('tr');

  if (currentRows.length >= 2) {

    tbody.removeChild(currentRows[0]);
  }


  const newRow = document.createElement('tr');


  const timeCell = document.createElement('td');
  timeCell.textContent = time;

  const destCell = document.createElement('td');
  destCell.textContent = destination;

  const remarkCell = document.createElement('td');
  remarkCell.textContent = remark;

  newRow.appendChild(timeCell);
  newRow.appendChild(destCell);
  newRow.appendChild(remarkCell);

  tbody.appendChild(newRow);
}


// To start a new game

document.addEventListener('submit', async function (event) {

  if (event.target.classList.contains('start-game-form')) {
    event.preventDefault();

    const airportIdent = document.querySelector('input[name=startGameIdent]').value;
    const startGameIsoCountry = document.querySelector('input[name=startGameIsoCountry]').value;
    const startGameMunicipality = document.querySelector('input[name=startGameMunicipality]').value;
    const startGameCountryName = document.querySelector('input[name=startGameCountryName]').value;

    const response = await fetch('/newgame', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ airport: airportIdent }),
    });

    const result = await response.json();

    if (result.success === true) {

      const popup1 = document.getElementById('popup1');
      popup1.classList.add('show');
      window.gameroute = true

      const remark = "On time";

      addRowToTable(result.start_time, startGameMunicipality, remark);

    } else {
      console.log(result.message);
    }
  } else if (event.target.classList.contains('load-game-form')) {
    event.preventDefault();

    const last_game_id = document.querySelector('input[name=loadGameId]').value;
    const last_level_reached = document.querySelector('input[name=lastLevelReached]').value;



    const response = await fetch('/loadgame', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ last_game_id: last_game_id }),
    });

    const result = await response.json();

    if (result.success === true) {

      // If new game is created, we are ready to start part one

      if (last_level_reached === "1") {

        console.log(last_level_reached)

        showPopup("popup2");

      } else if (last_level_reached === "2") {

        showPopup("popup3");
      }

    } else {
      console.log(result.message);
    }
  }
});

document.querySelectorAll('.reload_map').forEach(button => {
  button.addEventListener('click', async function (evt) {

    evt.preventDefault();

    markers.clearLayers();

    const response = await fetch('/reload_map', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const result = await response.json();
    console.log(result);

    if (result.success === true) {

      // loginMessage.innerText = `${result.message}
      // Your name: ${result.username},
      // Your airport: ${result.airport_name},
      // Airport ident: ${result.airport_ident}`;
      console.log(result.random_airports);
      console.log(result);

      // Actions with the map

      const greenMarker = L.ExtraMarkers.icon({
        icon: 'fa-home',
        markerColor: 'green',
        shape: 'star',
        prefix: 'fa',
      });

      if (result.last_ident) {

        const redMarker = L.ExtraMarkers.icon({
          icon: 'fa-home',
          markerColor: 'red',
          shape: 'star',
          prefix: 'fa',
        });

        const lastCoordinates = [
          result.last_latitude_deg,
          result.last_longitude_deg];

        L.marker(lastCoordinates, { icon: redMarker }).addTo(markers)
          .bindPopup(`<div class="home_airport_pop">Last airport
                    <form class="load-game-form">
                            <input type="hidden" value="${result.last_game}" name="loadGameId">
                            <input type="hidden" value="${result.last_level_reached}" name="lastLevelReached">
                            <input type="submit" value="load game">
                        </form>
                    </div>`)
          .openPopup();
      }

      // Print 20 raandom airports
      result.random_airports.forEach((airport, index) => {

        const airportCoordinates = [airport.latitude_deg, airport.longitude_deg];

        L.marker(airportCoordinates).addTo(markers).
          bindPopup(`Airport: ${airport.name} (${airport.ident})
                    <div>
                        <form class="start-game-form">
                            <input type="hidden" value="${airport.ident}" name="startGameIdent">
                            <input type="hidden" value="${airport.iso_country}" name="startGameIsoCountry">
                            <input type="hidden" value="${airport.municipality}" name="startGameMunicipality">
                            <input type="hidden" value="${airport.country_name}" name="startGameCountryName">
                            <input type="submit" value="Start a new game">
                        </form>
                    </div>`).
          openPopup();
      });

      // Popup for the home airport

      const homeCoordinates = [result.latitude_deg, result.longitude_deg];

      L.marker(homeCoordinates, { icon: greenMarker }).addTo(markers).
        bindPopup(`<div class="home_airport_pop">Home airport</div>`).
        openPopup();
    }
  });
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 5,
}).addTo(map);
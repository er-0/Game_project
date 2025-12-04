const map = L.map('map').setView([60.223876, 24.758061], 5);

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
        loginMessage.innerText = `${result.message}
        Your name: ${result.username},
        Your airport: ${result.airport_name},
        Airport ident: ${result.airport_ident}`;
        console.log(result.random_airports)
        console.log(result)

        // Actions with the map

        const greenMarker = L.ExtraMarkers.icon({
            icon: 'fa-home',
            markerColor: 'green',
            shape: 'star',
            prefix: 'fa'
        });

        if (result.last_ident) {

            const redMarker = L.ExtraMarkers.icon({
                icon: 'fa-home',
                markerColor: 'red',
                shape: 'star',
                prefix: 'fa'
            });

            const lastCoordinates = [result.last_latitude_deg, result.last_longitude_deg];

            L.marker(lastCoordinates, { icon: redMarker }).addTo(map)
                .bindPopup(`<div class="home_airport_pop">Last airport</div>`)
                .openPopup();
        }

        // Print 20 raandom airports
        result.random_airports.forEach((airport, index) => {

            const airportCoordinates = [airport.latitude_deg, airport.longitude_deg];

            L.marker(airportCoordinates).addTo(map)
                .bindPopup(`Airport: ${airport.name} (${airport.ident})
                    <div>
                        <form class="start-game-form">
                            <input type="hidden" value="${airport.ident}" name="startGameIdent">
                            <input type="submit" value="Start a new game">
                        </form>
                    </div>`)
                .openPopup();
        });

        // Popup for the home airport

        const homeCoordinates = [result.latitude_deg, result.longitude_deg];

        L.marker(homeCoordinates, { icon: greenMarker }).addTo(map)
            .bindPopup(`<div class="home_airport_pop">Home airport</div>`)
            .openPopup();
    }
    else {
        loginMessage.innerText = `${result.message}`;
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
        registerMessage.innerText = `${result.message}
        Your name: ${result.username},
        Your airport: ${result.airport_name},
        Airport ident: ${result.airport_ident}`;
        console.log(result.random_airports)

        // Actions with the map

        result.random_airports.forEach((airport, index) => {

            const airportCoordinates = [airport.latitude_deg, airport.longitude_deg];

            // Print 20 raandom airports
            L.marker(airportCoordinates).addTo(map)
                .bindPopup(`Airport: ${airport.name} (${airport.ident})
                    <div>
                        <form class="start-game-form">
                            <input type="hidden" value="${airport.ident}" name="startGameIdent">
                            <input type="submit" value="Start a new game">
                        </form>
                    </div>`)
                .openPopup();

            // Popup for the home airport

            const homeCoordinates = [result.latitude_deg, result.longitude_deg]

            L.marker(homeCoordinates).addTo(map)
                .bindPopup('Home airport')
                .openPopup();
        });
    }
    else {
        registerMessage.innerText = `${result.message}`;
        console.log(result.message);
    }
});

// To start a new game

document.addEventListener('submit', async function (event) {

    if (event.target.classList.contains('start-game-form')) {
        event.preventDefault();

        const airportIdent = document.querySelector('input[name=startGameIdent]').value;

        const response = await fetch('/newgame', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ airport: airportIdent }),
        });

        const result = await response.json();

        if (result.success === true) {
            console.log(result.game_id);
        } else {
            console.log(result.message);
        }
    }
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 5
}).addTo(map);

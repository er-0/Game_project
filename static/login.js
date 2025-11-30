const map = L.map('map').setView([60.223876, 24.758061], 13);


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

        // Actions with the map

        const homeCoordinates = [result.latitude_deg, result.longitude_deg];

        L.marker(homeCoordinates).addTo(map)
            .bindPopup('Home airport')
            .openPopup();

        result.random_airports.forEach((airport, index) => {

            const airportCoordinates = [airport.latitude_deg, airport.longitude_deg];

            L.marker(airportCoordinates).addTo(map)
                .bindPopup(`Airport: ${airport.name} (${airport.ident})`)
                .openPopup();
        });


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

        const homeCoordinates = [result.latitude_deg, result.longitude_deg]

        L.marker(homeCoordinates).addTo(map)
            .bindPopup('Home airport')
            .openPopup();

        result.random_airports.forEach((airport, index) => {

            const airportCoordinates = [airport.latitude_deg, airport.longitude_deg];

            L.marker(airportCoordinates).addTo(map)
                .bindPopup(`Airport: ${airport.name} (${airport.ident})`)
                .openPopup();
        });
    }
    else {
        registerMessage.innerText = `${result.message}`;
        console.log(result.message);
    }
});

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

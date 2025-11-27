
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

    if (result.success === true) {
        loginMessage.innerText = `${result.message}
        Your name: ${result.username},
        Your airport: ${result.airport_name},
        Airport ident: ${result.airport_ident}`;
        console.log(result.username)
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

    if (result.success === true) {
        registerMessage.innerText = `${result.message}
        Your name: ${result.username},
        Your airport: ${result.airport_name},
        Airport ident: ${result.airport_ident}`;
        console.log(result.username)
    }
    else {
        registerMessage.innerText = `${result.message}`;
        console.log(result.message);
    }
});


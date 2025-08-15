document.addEventListener('DOMContentLoaded', function() {
    // THE ID HAS BEEN CORRECTED HERE
    const movieGrid = document.getElementById('movie-grid');
    const authContainer = document.getElementById('auth-container');
    const authModal = new bootstrap.Modal(document.getElementById('authModal'));

    // Forms inside the modal
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const loginFormContainer = document.getElementById('login-form-container');
    const signupFormContainer = document.getElementById('signup-form-container');

    // Form Messages
    const loginError = document.getElementById('login-error');
    const signupMessage = document.getElementById('signup-message');

    // Links to switch forms
    const showSignupBtn = document.getElementById('show-signup');
    const showLoginBtn = document.getElementById('show-login');

    // --- 1. AUTH STATE & NAVBAR ---
    function updateAuthState() {
        const accessToken = localStorage.getItem('accessToken');
        const username = localStorage.getItem('username');

        if (accessToken && username) {
            authContainer.innerHTML = `
                <span class="navbar-text me-3">Welcome, ${username}</span>
                <button id="logout-btn" class="btn btn-outline-light btn-sm">Logout</button>
            `;
            document.getElementById('logout-btn').addEventListener('click', () => {
                localStorage.clear();
                updateAuthState();
            });
        } else {
            authContainer.innerHTML = `
                <button class="btn btn-join ms-2" id="join-now-btn">Join Now</button>
            `;
            document.getElementById('join-now-btn').addEventListener('click', (e) => {
                e.preventDefault();
                showSignupForm();
                authModal.show();
            });
        }
    }

    // --- 2. MODAL FORM SWITCHING ---
    function showLoginForm() {
        loginFormContainer.classList.remove('d-none');
        signupFormContainer.classList.add('d-none');
    }
    function showSignupForm() {
        signupFormContainer.classList.remove('d-none');
        loginFormContainer.classList.add('d-none');
    }
    showSignupBtn.addEventListener('click', (e) => { e.preventDefault(); showSignupForm(); });
    showLoginBtn.addEventListener('click', (e) => { e.preventDefault(); showLoginForm(); });


    // --- 3. FETCH MOVIES ---
    function fetchMovies() {
        if (!movieGrid) return;
        fetch('/api/movies/')
            .then(response => response.json())
            .then(movies => {
                movieGrid.innerHTML = '';
                movies.forEach(movie => {
                    const imageUrl = movie.poster_image
                        ? `${window.location.origin}${movie.poster_image}`
                        : 'https://placehold.co/400x600?text=No+Image';
                    const movieCard = `
                        <div class="col">
                            <div class="card movie-card h-100">
                                <img src="${imageUrl}" class="card-img-top" alt="${movie.title}">
                                <div class="card-body movie-card-body">
                                    <h5 class="card-title">${movie.title}</h5>
                                    <button class="btn btn-book w-100 mt-3 book-now-btn" data-movie-id="${movie.id}">Book Now</button>
                                </div>
                            </div>
                        </div>
                    `;
                    movieGrid.innerHTML += movieCard;
                });
                addBookingButtonListeners();
            })
            .catch(error => console.error('Error fetching movies:', error));
    }

    // --- 4. HANDLE BOOKING CLICKS ---
    function addBookingButtonListeners() {
        document.querySelectorAll('.book-now-btn').forEach(button => {
            button.addEventListener('click', function() {
                const movieId = this.dataset.movieId;
                const accessToken = localStorage.getItem('accessToken');

                if (accessToken) {
                    // If logged in, redirect to a booking page (we'll build this later)
                    window.location.href = `/booking/${movieId}/`;
                } else {
                    // If not logged in, show the signup/login modal
                    showSignupForm(); // Show signup form first for new users
                    authModal.show();
                }
            });
        });
    }

    // --- 5. HANDLE LOGIN & SIGNUP SUBMISSIONS ---
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            loginError.textContent = '';
            const username = document.getElementById('login-username').value;
            const password = document.getElementById('login-password').value;

            fetch('/api/users/token/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            })
            .then(response => {
                if (!response.ok) throw new Error('Invalid credentials.');
                return response.json();
            })
            .then(data => {
                localStorage.setItem('accessToken', data.access);
                localStorage.setItem('username', username);
                authModal.hide();
                updateAuthState();
            })
            .catch(error => {
                loginError.textContent = error.message;
            });
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            signupMessage.textContent = '';
            const username = document.getElementById('signup-username').value;
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;

            fetch('/api/users/register/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            })
            .then(response => {
                if (response.status === 201) {
                     signupMessage.textContent = 'Success! Please login.';
                     signupMessage.className = 'text-success';
                     setTimeout(() => showLoginForm(), 1500);
                } else {
                    return response.json().then(err => { throw new Error(Object.values(err).join(' ')) });
                }
            })
            .catch(error => {
                signupMessage.textContent = `Error: ${error.message}`;
                signupMessage.className = 'text-danger';
            });
        });
    }

    // --- INITIAL PAGE LOAD ---
    updateAuthState();
    fetchMovies();
});

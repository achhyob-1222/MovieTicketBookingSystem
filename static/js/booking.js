document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('booking-page-container');

    // This check prevents the script from running on the wrong page
    if (!container) {
        return;
    }

    const movieId = window.location.pathname.split('/')[2];
    const SEAT_PRICE = 350;
    let selectedShowtimeId = null;
    let selectedSeats = [];
    let selectedSeatNumbers = [];

    // Fetch movie details first
    fetch(`/api/movies/${movieId}/`)
        .then(res => {
            if (!res.ok) throw new Error('Movie not found');
            return res.json();
        })
        .then(movie => {
            renderBookingPage(movie);
            fetchShowtimes(movie.id);
        })
        .catch(error => {
            container.innerHTML = `<div class="container text-center py-5"><h2 class="text-danger">${error.message}</h2></div>`;
        });

    function renderBookingPage(movie) {
        const heroImageUrl = movie.hero_image ? movie.hero_image : '';
        container.innerHTML = `
            <section class="booking-hero" style="background-image: url('${heroImageUrl}')">
                <div class="container position-relative">
                    <h1 class="booking-movie-title">${movie.title}</h1>
                    <p>${movie.genre} | ${movie.duration} mins</p>
                </div>
            </section>
            <section class="py-5">
                <div class="container">
                    <div class="row g-5">
                        <div class="col-lg-8">
                            <h2 class="section-title mb-4">Select Showtime & Seats</h2>
                            <div id="showtimes-container" class="mb-4"></div>
                            <div id="seat-map-container" class="d-none">
                                <div class="screen-arc"></div>
                                <div class="seat-map" id="seat-map"></div>
                                <div class="seat-legend mt-4">
                                    <div class="legend-item"><div class="legend-box" style="background: #4a4a4a;"></div> Available</div>
                                    <div class="legend-item"><div class="legend-box" style="background: #3183FF;"></div> Selected</div>
                                    <div class="legend-item"><div class="legend-box" style="background: #222;"></div> Reserved</div>
                                </div>
                            </div>
                        </div>
                        <div class="col-lg-4">
                            <div class="p-4 bg-darker rounded">
                                <h3 class="section-title">Your Booking</h3>
                                <hr class="border-secondary"/>
                                <p><strong>Movie:</strong> ${movie.title}</p>
                                <p><strong>Showtime:</strong> <span id="showtime-display">Select a time</span></p>
                                <p><strong>Seats:</strong> <span id="selected-seats-display">None</span></p>
                                <hr class="border-secondary"/>
                                <h4 class="d-flex justify-content-between"><strong>Total:</strong> <span>Rs. <span id="total-price-display">0</span></span></h4>
                                <button id="confirm-booking-btn" class="btn btn-primary w-100 mt-3" disabled>Confirm Booking</button>
                                <p id="booking-message" class="mt-2"></p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        `;
    }

    function fetchShowtimes(movieId) {
        fetch(`/api/bookings/movies/${movieId}/showtimes/`)
            .then(res => res.json())
            .then(showtimes => {
                const showtimesContainer = document.getElementById('showtimes-container');
                let html = '<h4>Showtimes:</h4>';
                showtimes.forEach(st => {
                    const time = new Date(st.show_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                    html += `<button class="btn btn-outline-light me-2 mb-2 showtime-btn" data-showtime-id="${st.id}" data-showtime-text="${time}">${time}</button>`;
                });
                showtimesContainer.innerHTML = html;
                addShowtimeListeners();
            });
    }

    function addShowtimeListeners() {
        document.querySelectorAll('.showtime-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.showtime-btn.active').forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                selectedShowtimeId = this.dataset.showtimeId;
                document.getElementById('showtime-display').textContent = this.dataset.showtimeText;
                document.getElementById('seat-map-container').classList.remove('d-none');
                fetchSeats(selectedShowtimeId);
            });
        });
    }

    function fetchSeats(showtimeId) {
        const seatMap = document.getElementById('seat-map');
        seatMap.innerHTML = '<div class="spinner-border text-primary"></div>';
        selectedSeats = [];
        selectedSeatNumbers = [];
        updateBookingSummary();

        fetch(`/api/bookings/showtimes/${showtimeId}/seats/`)
            .then(res => res.json())
            .then(seats => {
                seatMap.innerHTML = '';
                seats.forEach(seat => {
                    const seatDiv = document.createElement('div');
                    seatDiv.classList.add('seat');
                    seatDiv.dataset.seatId = seat.id;
                    seatDiv.dataset.seatNumber = `${seat.seat_row}${seat.seat_number}`;
                    if (seat.is_booked) {
                        seatDiv.classList.add('booked');
                    } else {
                        seatDiv.addEventListener('click', toggleSeatSelection);
                    }
                    seatMap.appendChild(seatDiv);
                });
            });
    }

    function toggleSeatSelection(e) {
        const seatDiv = e.target;
        const seatId = parseInt(seatDiv.dataset.seatId);
        const seatNumber = seatDiv.dataset.seatNumber;

        const index = selectedSeats.indexOf(seatId);
        if (index > -1) {
            selectedSeats.splice(index, 1);
            selectedSeatNumbers.splice(index, 1);
            seatDiv.classList.remove('selected');
        } else {
            selectedSeats.push(seatId);
            selectedSeatNumbers.push(seatNumber);
            seatDiv.classList.add('selected');
        }
        updateBookingSummary();
    }

    function updateBookingSummary() {
        const seatsDisplay = document.getElementById('selected-seats-display');
        const priceDisplay = document.getElementById('total-price-display');
        const confirmBtn = document.getElementById('confirm-booking-btn');

        seatsDisplay.textContent = selectedSeatNumbers.length > 0 ? selectedSeatNumbers.join(', ') : 'None';
        priceDisplay.textContent = selectedSeats.length * SEAT_PRICE;
        confirmBtn.disabled = selectedSeats.length === 0;

        if (!confirmBtn.dataset.listener) {
             confirmBtn.addEventListener('click', handleBooking);
             confirmBtn.dataset.listener = 'true';
        }
    }

    function handleBooking() {
        const accessToken = localStorage.getItem('accessToken');
        const messageEl = document.getElementById('booking-message');

        fetch('/api/bookings/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                showtime_id: selectedShowtimeId,
                seats: selectedSeats
            })
        })
        .then(response => {
            if (response.ok) return response.json();
            return response.json().then(err => { throw new Error(JSON.stringify(err)) });
        })
        .then(data => {
            messageEl.textContent = 'Booking successful!';
            messageEl.className = 'mt-2 text-success';
            fetchSeats(selectedShowtimeId);
        })
        .catch(error => {
            messageEl.textContent = `Booking failed. Please try again.`;
            messageEl.className = 'mt-2 text-danger';
        });
    }
});
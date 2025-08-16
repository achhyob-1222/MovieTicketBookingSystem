document.addEventListener('DOMContentLoaded', function() {
    const ticketsList = document.getElementById('tickets-list');
    const accessToken = localStorage.getItem('accessToken');

    if (!accessToken) {
        window.location.href = '/'; // Redirect if not logged in
        return;
    }

    function fetchTickets() {
        ticketsList.innerHTML = '<div class="col-12 text-center"><div class="spinner-border text-primary"></div></div>';

        fetch('/api/bookings/my-tickets/', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Could not fetch tickets.');
            return response.json();
        })
        .then(bookings => {
            if (bookings.length === 0) {
                ticketsList.innerHTML = '<div class="col-12"><p class="text-white-50">You have no upcoming bookings.</p></div>';
                return;
            }

            ticketsList.innerHTML = '';
            bookings.forEach(booking => {
                const showDate = new Date(booking.showtime.date).toLocaleDateString([], { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
                const timeString = booking.showtime.time;
                const [hours, minutes] = timeString.split(':');
                const showTime = new Date(0, 0, 0, hours, minutes).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });

                const ticketCard = `
                    <div class="col-md-6">
                        <div class="card bg-darker text-white h-100">
                            <div class="card-body">
                                <h5 class="card-title text-primary">${booking.showtime.movie.title}</h5>
                                <p class="card-text mb-1">
                                    <strong>Hall:</strong> ${booking.showtime.hall.name}
                                </p>
                                <p class="card-text mb-1">
                                    <strong>Date:</strong> ${showDate}
                                </p>
                                <p class="card-text mb-1">
                                    <strong>Time:</strong> ${showTime}
                                </p>
                                <p class="card-text">
                                    <strong>Seats:</strong> ${booking.booked_seats.map(s => s.seat_label).join(', ')}
                                </p>
                                <button class="btn btn-sm btn-outline-danger cancel-btn" data-booking-id="${booking.id}">Cancel Booking</button>
                            </div>
                        </div>
                    </div>
                `;
                ticketsList.innerHTML += ticketCard;
            });
            addCancelListeners();
        })
        .catch(error => {
            ticketsList.innerHTML = `<div class="col-12"><p class="text-danger">${error.message}</p></div>`;
        });
    }

    function addCancelListeners() {
        document.querySelectorAll('.cancel-btn').forEach(button => {
            button.addEventListener('click', function() {
                const bookingId = this.dataset.bookingId;
                if (confirm('Are you sure you want to cancel this booking?')) {
                    cancelBooking(bookingId);
                }
            });
        });
    }

    function cancelBooking(bookingId) {
        fetch(`/api/bookings/${bookingId}/cancel/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'X-CSRFToken': getCookie('csrftoken') // For Django's CSRF protection
            }
        })
        .then(response => {
            if (response.status === 204) { // 204 No Content is a successful deletion
                alert('Booking cancelled successfully.');
                fetchTickets(); // Refresh the list
            } else {
                alert('Failed to cancel booking.');
            }
        });
    }

    // Helper function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    fetchTickets();
});
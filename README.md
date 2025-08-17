CineWave - Movie Ticket Booking System
CineWave is a full-featured web application for browsing movies and booking tickets, built with Python and Django. It features a modern, single-page-style frontend that communicates with a powerful REST API backend.

✨ Features
User Authentication: Secure user registration and login using JSON Web Tokens (JWT).

Dynamic Movie Listings: The homepage automatically separates movies into "Now Showing" and "Coming Soon" sections based on their release dates.

Detailed Booking Page: A dedicated page for each movie, showing a hero banner, synopsis, and an embedded YouTube trailer.

Interactive Seat Selection: A visual seat map that allows users to select available seats and see which ones are already reserved.

Flexible Showtime Management: A custom admin panel that allows administrators to easily create and manage showtimes for different halls and dates.

"Your Tickets" Page: A user-specific page to view all upcoming bookings with the option to cancel them.

🛠️ Tech Stack
Backend: Python, Django, Django Rest Framework (DRF)

Authentication: DRF Simple JWT

Database: SQLite3 (for development)

Frontend: Django Templates, Bootstrap 5, JavaScript

Image Handling: Pillow

🚀 Setup and Installation
Follow these steps to get the project running on your local machine.

1. Prerequisites
Python 3.8 or higher

pip (Python package installer)

2. Clone the Repository
git clone <your-repository-url> || https://github.com/achhyob-1222/MovieTicketBookingSystem.git
cd <your-project-directory>


3. Set Up a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

Create the environment:

python -m venv .venv


Activate the environment:

On Windows:

.\.venv\Scripts\activate


On macOS/Linux:

source .venv/bin/activate


4. Install Dependencies
Install all the required Python packages using the requirements.txt file.

pip install -r requirements.txt


5. Set Up the Database
Run the migrations to create the database tables for all the apps.

python manage.py makemigrations
python manage.py migrate


6. Create a Superuser
This creates an admin account so you can log in to the Django admin panel.

python manage.py createsuperuser


Follow the prompts to create your username and password.

7. Run the Development Server
python manage.py runserver


The application will now be running at http://127.0.0.1:8000/.

📋 Usage
Start the server using the command above.

Access the Admin Panel: Navigate to http://127.0.0.1:8000/admin/ and log in with your superuser account.

Create Cinema Halls: Before adding movies, go to the "Cinema halls" section and create your halls (e.g., "Hall A", "Hall B"). The seats will be created automatically by a signal.

Add Movies: Go to the "Movies" section and add new movies. Fill in all the details, including release dates and image URLs.

Create Showtimes: Go to the "Showtimes" section to schedule when and where each movie will be shown.

View the Website: Navigate to http://127.0.0.1:8000/ to see the public-facing website, browse movies, and book tickets.
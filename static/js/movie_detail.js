document.addEventListener('DOMContentLoaded', function() {
    // This script now only runs on the movie detail page.
    const container = document.getElementById('movie-detail-container');
    const pathParts = window.location.pathname.split('/');
    const movieId = pathParts[2];

    if (!movieId) {
        container.innerHTML = `<div class="container text-center py-5"><h2 class="text-danger">Could not find Movie ID in the URL.</h2></div>`;
        return;
    }

    // Fetch details for this specific movie
    fetch(`/api/movies/${movieId}/`)
        .then(response => {
            if (!response.ok) throw new Error('Movie not found');
            return response.json();
        })
        .then(movie => {
            renderMovieDetail(movie);
        })
        .catch(error => {
            container.innerHTML = `<div class="container text-center py-5"><h2 class="text-danger">${error.message}</h2></div>`;
        });

    function renderMovieDetail(movie) {
        const heroImageUrl = movie.hero_image || 'https://placehold.co/1920x1080/1c1c1c/ffffff?text=No+Banner';
        const posterImageUrl = movie.poster_image || 'https://placehold.co/400x600/1c1c1c/ffffff?text=No+Poster';

        let trailerEmbedUrl = '';
        if (movie.trailer_urls) {
            try {
                const url = new URL(movie.trailer_urls);
                const videoId = url.searchParams.get('v');
                if (videoId) {
                    trailerEmbedUrl = `https://www.youtube.com/embed/${videoId}`;
                }
            } catch (e) {
                console.error('Invalid trailer URL:', movie.trailer_urls);
            }
        }

        container.innerHTML = `
            <section class="booking-hero" style="background-image: url('${heroImageUrl}')">
                <div class="container position-relative">
                    <h1 class="booking-movie-title">${movie.title || 'Title Not Available'}</h1>
                    <p>
                        ${movie.genre || 'N/A'} | 
                        ${movie.duration || 'N/A'} mins | 
                        Released: ${movie.release_date || 'N/A'}
                    </p>
                </div>
            </section>
            <section class="py-5">
                <div class="container">
                    <div class="row">
                        <div class="col-lg-8">
                            <h2 class="section-title mb-3">Synopsis</h2>
                            <p class="text-white-50">${movie.description || 'No description available.'}</p>
                            
                            ${trailerEmbedUrl ? `
                                <h2 class="section-title mt-5 mb-3">Trailer</h2>
                                <div class="ratio ratio-16x9">
                                    <iframe src="${trailerEmbedUrl}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                                </div>
                            ` : '<p class="text-white-50 mt-5">No trailer available for this movie.</p>'}
                        </div>
                        <div class="col-lg-4">
                            <img src="${posterImageUrl}" class="img-fluid rounded" alt="Poster for ${movie.title || 'Movie'}">
                        </div>
                    </div>
                </div>
            </section>
        `;
    }
});
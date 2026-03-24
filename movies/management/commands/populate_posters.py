# movies/management/commands/populate_posters.py
from django.core.management.base import BaseCommand
from movies.models import Movie
from django.conf import settings
import requests
import time
from requests.adapters import HTTPAdapter, Retry
from django.db.models import Q
import re
from rapidfuzz import fuzz

DEFAULT_POSTER = "https://via.placeholder.com/200x250?text=No+Poster"

def fetch_tmdb_poster(title, year=None):
    """
    Fetch poster URL from TMDb for a movie title and optional year.
    Uses fuzzy matching to pick best result.
    Returns None if not found.
    """
    url = f"{settings.TMDB_BASE_URL}/search/movie"
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1)
    session.mount("https://", HTTPAdapter(max_retries=retries))

    try:
        response = session.get(
            url,
            params={"api_key": settings.TMDB_API_KEY, "query": title, "year": year},
            timeout=10
        )
        if response.status_code != 200:
            print(f"TMDb request failed for '{title}': {response.status_code}")
            return None

        results = response.json().get("results", [])
        if not results:
            return None

        # Fuzzy match the best movie title
        best_match = None
        highest_score = 0
        for movie in results:
            movie_title = movie.get('title', '')
            score = fuzz.ratio(title.lower(), movie_title.lower())
            if score > highest_score:
                best_match = movie
                highest_score = score

        if best_match and best_match.get('poster_path'):
            return f"{settings.TMDB_IMAGE_BASE}{best_match['poster_path']}"

        return None

    except Exception as e:
        print(f"Error fetching '{title}': {e}")
        return None


def normalize_title(title):
    """Remove punctuation and lowercase for fallback searches."""
    return re.sub(r'[^\w\s]', '', title).lower()


class Command(BaseCommand):
    help = "Populate or refresh poster URLs from TMDb using fuzzy matching and retries."

    def add_arguments(self, parser):
        parser.add_argument(
            '--force', action='store_true',
            help='Force refresh posters for all movies, even if they have one.'
        )

    def handle(self, *args, **kwargs):
        force = kwargs.get('force', False)

        if force:
            movies = Movie.objects.all()
        else:
            movies = Movie.objects.filter(
                Q(poster_url__isnull=True) | Q(poster_url=DEFAULT_POSTER)
            )

        total = movies.count()
        if total == 0:
            self.stdout.write("No movies need poster updates")
            return

        self.stdout.write(f"Updating posters for {total} movies...")

        failed_movies = []

        for i, movie in enumerate(movies, start=1):
            poster = fetch_tmdb_poster(movie.title, getattr(movie, 'year', None))

            # Retry without year
            if not poster:
                poster = fetch_tmdb_poster(movie.title)

            # Retry with normalized title
            if not poster:
                normalized = normalize_title(movie.title)
                poster = fetch_tmdb_poster(normalized)

            if poster:
                movie.poster_url = poster
                movie.save(update_fields=["poster_url"])
            else:
                failed_movies.append(movie.title)
                continue

            movie.poster_url = poster
            movie.save(update_fields=["poster_url"])
            self.stdout.write(f"[{i}/{total}] Updated: {movie.title} -> {poster}")
            time.sleep(1)  # Respect TMDb rate limits

        self.stdout.write("Done!")
        if failed_movies:
            self.stdout.write("Movies still missing posters after all attempts:")
            for title in failed_movies:
                self.stdout.write(f"- {title}")
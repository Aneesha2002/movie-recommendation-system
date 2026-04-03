import time
import re
import logging
import requests
from requests.adapters import HTTPAdapter, Retry
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q
from rapidfuzz import fuzz
from movies.models import Movie

# Default poster if all attempts fail
DEFAULT_POSTER = "https://via.placeholder.com/200x250?text=No+Poster"

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def normalize_title(title: str) -> str:
    """
    Remove punctuation, extra spaces, and text in parentheses for fallback searches.
    """
    title = re.sub(r'\s*\(.*?\)\s*', '', title)  # remove parentheses
    title = re.sub(r'[^\w\s]', '', title)  # remove punctuation
    return title.strip().lower()

def fetch_tmdb_poster(title: str, year: int = None) -> str | None:
    """
    Fetch poster URL from TMDb using fuzzy matching.
    Returns None if no poster found.
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
            logging.warning(f"TMDb request failed for '{title}': {response.status_code}")
            return None

        results = response.json().get("results", [])
        if not results:
            return None

        # Find best fuzzy match
        best_match = None
        highest_score = 0
        for movie in results:
            movie_title = movie.get("title", "")
            score = fuzz.ratio(title.lower(), movie_title.lower())
            if score > highest_score:
                best_match = movie
                highest_score = score

        if best_match and best_match.get("poster_path"):
            return f"{settings.TMDB_IMAGE_BASE}{best_match['poster_path']}"

        return None

    except Exception as e:
        logging.error(f"Error fetching '{title}': {e}")
        return None

class Command(BaseCommand):
    help = "Automatically populate or refresh poster URLs from TMDb using fuzzy matching and retries."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force refresh posters for all movies, even if they already have one."
        )

    def handle(self, *args, **kwargs):
        force = kwargs.get("force", False)

        if force:
            movies = Movie.objects.all()
        else:
            movies = Movie.objects.filter(Q(poster_url__isnull=True) | Q(poster_url=DEFAULT_POSTER))

        total = movies.count()
        if total == 0:
            logging.info("No movies need poster updates.")
            return

        logging.info(f"Updating posters for {total} movies...")
        failed_movies = []

        for i, movie in enumerate(movies, start=1):
            poster = fetch_tmdb_poster(movie.title, movie.release_year)

            # Fallback: normalized title without punctuation/parentheses
            if not poster:
                normalized = normalize_title(movie.title)
                poster = fetch_tmdb_poster(normalized, movie.release_year)
            if not poster:
                poster = fetch_tmdb_poster(normalized)  # ignore year
            if not poster:
                poster = DEFAULT_POSTER
                failed_movies.append(movie.title)

            movie.poster_url = poster
            movie.save(update_fields=["poster_url"])
            logging.info(f"[{i}/{total}] {movie.title} -> {poster}")
            time.sleep(1)  # polite TMDb API limit

        logging.info("Poster update completed.")
        if failed_movies:
            logging.warning("Movies still missing posters after all attempts:")
            for title in failed_movies:
                logging.warning(f"- {title}")
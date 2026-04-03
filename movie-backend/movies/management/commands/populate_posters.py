from django.core.management.base import BaseCommand
from movies.models import Movie
from django.conf import settings
import requests
import time
from requests.adapters import HTTPAdapter, Retry
from django.db.models import Q
import re
from rapidfuzz import fuzz
import logging

DEFAULT_POSTER = "https://via.placeholder.com/200x250?text=No+Poster"

logger = logging.getLogger(__name__)

# reuse one session instead of creating per request
session = requests.Session()
retries = Retry(total=3, backoff_factor=1)
session.mount("https://", HTTPAdapter(max_retries=retries))


def fetch_tmdb_poster(title, year=None):
    """
    Try to fetch a poster from TMDb.
    - Uses retries via session
    - Applies fuzzy matching to pick best result
    - Returns None if no reliable match
    """
    url = f"{settings.TMDB_BASE_URL}/search/movie"

    try:
        response = session.get(
            url,
            params={
                "api_key": settings.TMDB_API_KEY,
                "query": title,
                "year": year
            },
            timeout=10
        )

        if response.status_code != 200:
            logger.warning(f"TMDb failed for '{title}' ({response.status_code})")
            return None

        results = response.json().get("results", [])
        if not results:
            return None

        # pick best match based on fuzzy score
        best_match = None
        highest_score = 0

        for movie in results:
            movie_title = movie.get('title', '')
            score = fuzz.ratio(title.lower(), movie_title.lower())

            # ignore weak matches to avoid wrong posters
            if score > highest_score and score >= 70:
                highest_score = score
                best_match = movie

        if best_match and best_match.get('poster_path'):
            return f"{settings.TMDB_IMAGE_BASE}{best_match['poster_path']}"

        return None

    except Exception as e:
        logger.error(f"Error fetching '{title}': {e}")
        return None


def normalize_title(title):
    """Basic cleanup for fallback search (remove punctuation, lowercase)."""
    return re.sub(r'[^\w\s]', '', title).lower()


class Command(BaseCommand):
    help = "Populate or refresh poster URLs from TMDb"

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Refresh posters even if already present'
        )

    def handle(self, *args, **kwargs):
        force = kwargs.get('force', False)

        # only update missing posters unless forced
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
            # try strict match (title + year)
            poster = fetch_tmdb_poster(movie.title, movie.release_year)

            # fallback: title only
            if not poster:
                poster = fetch_tmdb_poster(movie.title)

            # fallback: normalized title
            if not poster:
                normalized = normalize_title(movie.title)
                poster = fetch_tmdb_poster(normalized)

            # final fallback
            if not poster:
                poster = DEFAULT_POSTER
                failed_movies.append(movie.title)

            movie.poster_url = poster
            movie.save(update_fields=["poster_url"])

            logger.info(f"{movie.title} -> {poster}")
            self.stdout.write(f"[{i}/{total}] Updated: {movie.title}")

            # basic rate limiting (TMDb can throttle)
            time.sleep(0.5)

        self.stdout.write("Done!")

        if failed_movies:
            self.stdout.write("\nStill missing posters:")
            for title in failed_movies:
                self.stdout.write(f"- {title}")
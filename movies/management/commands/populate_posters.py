from django.core.management.base import BaseCommand
from movies.models import Movie
from django.conf import settings
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def fetch_tmdb_poster(title, year=None):
    url = f"{settings.TMDB_BASE_URL}/search/movie"

    try:
        response = requests.get(
            url,
            params={
                "api_key": settings.TMDB_API_KEY,
                "query": title,
                "year": year 
            },
            timeout=10
        )

        results = response.json().get("results")

        if results:
            for movie in results:
                release_date = movie.get("release_date", "")
                if year and release_date.startswith(str(year)):
                    if movie.get("poster_path"):
                        return f"{settings.TMDB_IMAGE_BASE}{movie['poster_path']}"

            if results[0].get("poster_path"):
                return f"{settings.TMDB_IMAGE_BASE}{results[0]['poster_path']}"

    except Exception as e:
        print(f"Error fetching {title}: {e}")

    return None


class Command(BaseCommand): 
    help = "Populate missing poster URLs from TMDb"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.filter(poster_url__isnull=True) | Movie.objects.filter(poster_url="")

        total = movies.count()
        self.stdout.write(f"Found {total} movies without posters")

        for i, movie in enumerate(movies, start=1):
            poster = fetch_tmdb_poster(movie.title)

            if poster:
                movie.poster_url = poster
                movie.save(update_fields=["poster_url"])
                self.stdout.write(f"[{i}/{total}] Updated: {movie.title}")
            else:
                self.stdout.write(f"[{i}/{total}] Failed: {movie.title}")

            time.sleep(1) 

        self.stdout.write("Done!")
import csv
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre

DEFAULT_POSTER = "https://via.placeholder.com/200x250?text=No+Poster"

class Command(BaseCommand):
    help = 'Import movies from CSV'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path',
            type=str,
            help='Path to the CSV file containing movies'
        )

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        self.stdout.write(f"IMPORT STARTED: {csv_path}")

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                title = row['title']
                movie, created = Movie.objects.get_or_create(
                    title=title,
                    defaults={
                        'description': row.get('overview', ''),
                        'release_year': int(row.get('year', 2000)),
                        'language': row.get('language', 'en'),
                        'poster_url': DEFAULT_POSTER
                    }
                )

                genres = row.get('genre', '').split('|')
                for genre_name in genres:
                    genre_name = genre_name.strip()
                    if genre_name:
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                        movie.genres.add(genre)

                action = "Created" if created else "Skipped"
                self.stdout.write(f"{action}: {movie.title}")

        self.stdout.write("IMPORT FINISHED")
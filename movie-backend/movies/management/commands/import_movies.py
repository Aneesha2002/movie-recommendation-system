import csv
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from movies.models import Movie, Genre

DEFAULT_POSTER = "https://via.placeholder.com/200x250?text=No+Poster"

# Setup logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import movies from CSV with logging and error handling'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path',
            type=str,
            help='Path to the CSV file containing movies'
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']

        logger.info(f"IMPORT STARTED: {csv_path}")
        self.stdout.write(self.style.NOTICE(f"IMPORT STARTED: {csv_path}"))

        created_count = 0
        skipped_count = 0
        error_count = 0

        try:
            with open(csv_path, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        title = row.get('title', '').strip()
                        if not title:
                            raise ValueError("Missing title")

                        # Safe year parsing
                        year = row.get('year')
                        release_year = int(year) if year and year.isdigit() else None

                        movie, created = Movie.objects.get_or_create(
                            title=title,
                            release_year=release_year,
                            defaults={
                                'description': row.get('overview', '').strip(),
                                'language': row.get('language', 'en'),
                                'poster_url': DEFAULT_POSTER
                            }
                        )

                        # Handle genres
                        genres = row.get('genre', '').split('|')
                        for genre_name in genres:
                            genre_name = genre_name.strip()
                            if genre_name:
                                genre, _ = Genre.objects.get_or_create(name=genre_name)
                                movie.genres.add(genre)

                        if created:
                            created_count += 1
                            logger.info(f"Created movie: {movie.title}")
                            self.stdout.write(self.style.SUCCESS(f"Created: {movie.title}"))
                        else:
                            skipped_count += 1
                            logger.warning(f"Skipped existing movie: {movie.title}")
                            self.stdout.write(f"Skipped: {movie.title}")

                    except Exception as e:
                        error_count += 1
                        logger.error(f"Error processing row {row} -> {e}")
                        self.stdout.write(self.style.ERROR(f"Error: {row} -> {e}"))

        except FileNotFoundError:
            logger.critical(f"CSV file not found: {csv_path}")
            self.stdout.write(self.style.ERROR("CSV file not found"))
            return

        except Exception as e:
            logger.critical(f"Fatal error: {e}")
            self.stdout.write(self.style.ERROR(f"Fatal error: {e}"))
            return

        # Final summary
        logger.info(f"IMPORT COMPLETED: Created={created_count}, Skipped={skipped_count}, Errors={error_count}")

        self.stdout.write("\nIMPORT SUMMARY:")
        self.stdout.write(f"Created: {created_count}")
        self.stdout.write(f"Skipped: {skipped_count}")
        self.stdout.write(f"Errors: {error_count}")
        self.stdout.write(self.style.SUCCESS("IMPORT FINISHED"))
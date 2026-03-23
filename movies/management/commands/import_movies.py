import csv
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre


class Command(BaseCommand):
    help = 'Import movies from CSV'

    def handle(self, *args, **kwargs):
        print(" IMPORT STARTED")

        with open('data/movies.csv', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                print("ROW:", row)
          
                movie = Movie.objects.create(
            title=row['title'],
            description=row.get('overview', ''),
            release_year=int(row.get('year', 2000)),
            language=row.get('language', 'en'),  
            poster_url=''  
)

                print("CREATED:", movie.title)

                genres = row.get('genre', '').split('|')

                for genre_name in genres:
                    genre_name = genre_name.strip()
                    if genre_name:
                        genre, _ = Genre.objects.get_or_create(name=genre_name)
                        movie.genres.add(genre)

    print(" IMPORT FINISHED")
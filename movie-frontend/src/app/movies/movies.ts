// src/app/movies/movies.ts
import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api.service';
import { Subject, debounceTime } from 'rxjs';

interface Genre { id: number; name: string; }
interface Movie {
  id: number;
  title: string;
  description: string;
  release_year: number;
  genres: Genre[];
  poster_url: string;
  avg_rating: number;
  your_rating?: number;       
  recommendations?: Movie[];
}

@Component({
  selector: 'app-movies',
  standalone: true,
  imports: [CommonModule],
  template: `
<input type="text" placeholder="Search movies..." (input)="onSearch($event)" class="search-box" />

<h2>🔥 Trending</h2>
<div *ngIf="trending.length; else noTrending" class="trending-container">
  <div *ngFor="let movie of trending" class="movie-card">
    <img [src]="getPoster(movie)" alt="{{ movie.title }}" />
    <div class="hover-info">
      <h4>{{ movie.title }}</h4>
      <p>{{ movie.description }}</p>
      <p>Year: {{ movie.release_year }}</p>
      <p>Genres: {{ movie.genres.map(g => g.name).join(', ') }}</p>
      <p>Average Rating: {{ movie.avg_rating || "No ratings yet" }}</p>
    </div>
  </div>
</div>
<ng-template #noTrending>No trending movies available</ng-template>

<h2>🎯 Recommended For You</h2>
<div *ngIf="recommendedMovies.length; else noRecs" class="movies-grid">
  <div *ngFor="let movie of recommendedMovies" class="movie-card">
    <img [src]="getPoster(movie)" alt="{{ movie.title }}" />
    <div class="hover-info">
      <h4>{{ movie.title }}</h4>
    </div>
  </div>
</div>
<ng-template #noRecs>No recommendations available</ng-template>

<h2>🎬 All Movies ({{ movies.length }})</h2>
<div *ngIf="movies.length; else noMovies" class="movies-grid">
  <div *ngFor="let movie of movies; trackBy: trackById" class="movie-card">
    <img [src]="getPoster(movie)" alt="{{ movie.title }}" />
    <div class="hover-info">
      <h4>{{ movie.title }}</h4>
      <p>{{ movie.description }}</p>
      <p>Year: {{ movie.release_year }}</p>
      <p>Genres: {{ movie.genres.map(g => g.name).join(', ') }}</p>
      <p>Average Rating: {{ movie.avg_rating || "No ratings yet" }}</p>
      <p>
        Your Rating:
        <span *ngFor="let star of [1,2,3,4,5]"
              (click)="rateMovie(movie, star)"
              [style.color]="star <= (movie?.your_rating ?? 0) ? 'gold' : 'gray'">★</span>
      </p>
    </div>
  </div>
</div>
<ng-template #noMovies>No movies available</ng-template>
  `,
  styles: [`
.search-box { margin-bottom:1rem; padding:0.5rem; width:100%; max-width:400px; font-size:1rem; }
.movie-card { position: relative; width:200px; border-radius:8px; overflow:hidden; background:#f5f5f5; box-shadow:0 2px 6px rgba(0,0,0,0.15); text-align:center; cursor:pointer; transition: transform 0.2s, box-shadow 0.2s; }
.movie-card:hover { transform:translateY(-5px); box-shadow:0 6px 12px rgba(0,0,0,0.25); }
.movie-card img { width:100%; height:250px; object-fit:cover; }
.hover-info { padding:0.5rem; font-size:0.9rem; text-align:left; min-height:220px; }
.trending-container, .movies-grid { display:flex; gap:1rem; flex-wrap:wrap; justify-content:start; }
.recommendations { margin-top:0.5rem; }
.recommendations ul { padding-left:1rem; margin:0; max-height:70px; overflow-y:auto; }
  `]
})
export class MoviesComponent implements OnInit {
  searchSubject = new Subject<string>();
  movies: Movie[] = [];
  allMovies: Movie[] = [];
  trending: Movie[] = [];
recommendedMovies: any[] = [];
  constructor(private apiService: ApiService, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.loadMovies();
    this.loadTrending();
    
    this.apiService.getRecommendations().subscribe({
  next: (data) => {
    this.recommendedMovies = data as any[];
    this.cdr.detectChanges();
  },
  error: (err) => {
    console.error('Recommendations failed', err);
    this.recommendedMovies = [];
  }
});

    this.searchSubject.pipe(debounceTime(300)).subscribe(query => {
      const q = query?.toLowerCase() || '';
      this.movies = q
        ? this.allMovies.filter(m =>
            m.title.toLowerCase().includes(q) ||
            m.description.toLowerCase().includes(q) ||
            m.genres.some(g => g.name.toLowerCase().includes(q))
          )
        : [...this.allMovies];
      this.cdr.detectChanges();
    });
  }

 loadMovies() {
  this.apiService.getMovies().subscribe(data => {
    // Treat as paginated response if not array
    const moviesArray = Array.isArray(data)
      ? data
      : (data as { results?: any[] }).results ?? [];

    this.allMovies = moviesArray.map((m: any) => ({
      ...m,
      your_rating: m.your_rating ?? null,
    }));
    this.movies = [...this.allMovies];
    this.cdr.detectChanges();
  });
}

loadTrending() {
  this.apiService.getTrending().subscribe(data => {
    const trendingArray = Array.isArray(data)
      ? data
      : (data as { results?: any[] }).results ?? [];

    this.trending = trendingArray.map((m: any) => ({
      ...m,
      your_rating: m.your_rating ?? null,
    }));
    this.cdr.detectChanges();
  });
}

  onSearch(event: any) { this.searchSubject.next(event.target.value); }

  getPoster(movie: Movie) {
    return movie.poster_url?.trim() || 'https://via.placeholder.com/200x250?text=No+Poster';
  }

  trackById(index: number, movie: Movie) { return movie.id; }

  rateMovie(movie: Movie, value: number) {
    this.apiService.rateMovie(movie.id, value).subscribe({
      next: (res: any) => {
        if (!res.error) {
          movie.avg_rating = res.avg_rating;
          movie.your_rating = value;
        }
      },
      error: (err) => {
        console.error('Rating failed', err);
        alert('Failed to submit rating. Are you logged in?');
      }
    });
  }
}
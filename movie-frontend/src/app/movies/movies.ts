// src/app/movies/movies.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api.service';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-movies',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2>🔥 Trending</h2>
<div *ngIf="trending && trending.length > 0; else noTrending" class="trending-container">
  <div *ngFor="let movie of trending" class="trending-card">
    <div class="movie-info">
      <h3>{{ movie.title }}</h3>
     <p>Rating: {{ movie.avg_rating || 0 }}</p>
    </div>
  </div>
</div>
<ng-template #noTrending>No trending movies available 😔</ng-template>
<h2>🎬 Movies (Total: {{ movies?.length || 0 }})</h2>
<div *ngIf="movies && movies.length > 0; else noMovies" class="movies-grid">
  <div *ngFor="let movie of movies" class="movie-card">
    
    <h4>{{ movie.title }}</h4>
    <p>Rating: {{ movie.avg_rating || 0 }}</p>
  </div>
</div>
<ng-template #noMovies>No movies available 😔</ng-template>
  `,
  styles: [`
    .trending-container {
  display: flex;
  overflow-x: auto;
  gap: 1rem;
  padding: 0.5rem 0;
}

.trending-card {
  min-width: 150px;
  border-radius: 8px;
  overflow: hidden;
  background: #f0f0f0;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  text-align: center;
  flex-shrink: 0;
}

.trending-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.trending-card .movie-info {
  padding: 0.5rem;
}

.movies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.movie-card {
  border-radius: 8px;
  overflow: hidden;
  background: #fafafa;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  text-align: center;
}

.movie-card img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}
  `]
})
export class MoviesComponent implements OnInit {
  movies: any[] = [];
  trending: any[] = [];

  
constructor(private apiService: ApiService, private cdr: ChangeDetectorRef) {}

ngOnInit() {
  this.apiService.getMovies().subscribe({
    next: data => {
      this.movies = Array.isArray(data) ? data : [];
      this.cdr.detectChanges(); // force Angular to update view
    },
    error: err => console.error('MOVIES LOAD ERROR:', err)
  });

  this.apiService.getTrending().subscribe({
    next: data => {
      this.trending = Array.isArray(data) ? data : [];
      this.cdr.detectChanges(); // force Angular to update view
    },
    error: err => console.error('TRENDING LOAD ERROR:', err)
  });
}
}
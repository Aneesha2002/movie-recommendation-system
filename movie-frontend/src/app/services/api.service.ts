import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  //  Base URL of your Django backend
  private baseUrl = 'https://movie-recommendation-system-cef2.onrender.com/api';

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  // --------------------------------------------------
  //  Get Authorization Header (if user is logged in)
  // --------------------------------------------------
  private getAuthHeaders(): HttpHeaders | null {
    const token = this.authService.getAccessToken();

    // If token exists → attach Bearer token
    if (token) {
      return new HttpHeaders({
        Authorization: `Bearer ${token}`
      });
    }

    // If not logged in → no headers
    return null;
  }

  // --------------------------------------------------
  //  Unified request options (cleaner usage)
  // --------------------------------------------------
  private getOptions() {
    const headers = this.getAuthHeaders();
    return headers ? { headers } : {};
  }

  // --------------------------------------------------
  //  Error handler for GET requests
  // DO NOT silently hide errors — log them properly
  // --------------------------------------------------
  private handleError<T>(operation: string) {
    return (error: any): Observable<T> => {
      console.error(`❌ ${operation} failed:`, error);

      // Optional: Customize based on status
      if (error.status === 0) {
        console.error('🌐 Network/CORS issue');
      } else if (error.status === 401) {
        console.error('🔐 Unauthorized request');
      } else if (error.status === 500) {
        console.error('🔥 Server error');
      }

      // Return empty fallback so UI doesn't crash
      return of([] as unknown as T);
    };
  }

  // --------------------------------------------------
  //  Get all movies
  // --------------------------------------------------
  getMovies(): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.baseUrl}/movies/`,
      this.getOptions()
    ).pipe(
      catchError(this.handleError<any[]>('getMovies'))
    );
  }

  // --------------------------------------------------
  //  Get trending movies
  // --------------------------------------------------
  getTrending(): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.baseUrl}/movies/trending/`,
      this.getOptions()
    ).pipe(
      catchError(this.handleError<any[]>('getTrending'))
    );
  }

  // --------------------------------------------------
  //  Search movies
  // --------------------------------------------------
  searchMovies(query: string): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.baseUrl}/movies/?search=${query}`,
      this.getOptions()
    ).pipe(
      catchError(this.handleError<any[]>('searchMovies'))
    );
  }

  // --------------------------------------------------
  //  Get single movie details
  // --------------------------------------------------
  getMovieById(id: number): Observable<any> {
    return this.http.get<any>(
      `${this.baseUrl}/movies/${id}/`,
      this.getOptions()
    ).pipe(
      catchError(this.handleError<any>('getMovieById'))
    );
  }

  // --------------------------------------------------
  //  Rate a movie (requires login)
  // --------------------------------------------------
  rateMovie(movieId: number, rating: number): Observable<any> {
    const token = this.authService.getAccessToken();

    // If user is not logged in → return error safely
    if (!token) {
      console.warn('⚠️ User not logged in');
      return of({ error: 'User not logged in' });
    }

    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });

    return this.http.post<any>(
      `${this.baseUrl}/movies/${movieId}/rate/`,
      { rating },
      { headers }
    );
  }

  // --------------------------------------------------
  //  Get personalized / fallback recommendations
  // --------------------------------------------------
  getRecommendations(): Observable<any[]> {
    return this.http.get<any[]>(
      `${this.baseUrl}/recommendations/`,
      this.getOptions()
    ).pipe(
      catchError(this.handleError<any[]>('getRecommendations'))
    );
  }
}
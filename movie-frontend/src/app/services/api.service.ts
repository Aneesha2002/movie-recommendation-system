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
      console.error(` ${operation} failed:`, error);

      // Optional: Customize based on status
      if (error.status === 0) {
        console.error(' Network/CORS issue');
      } else if (error.status === 401) {
        console.error(' Unauthorized request');
      } else if (error.status === 500) {
        console.error(' Server error');
      }

      // Return empty fallback so UI doesn't crash
      return of([] as unknown as T);
    };
  }

  // --------------------------------------------------
  //  Get all movies
  // --------------------------------------------------
 getMovies(search?: string): Observable<any[]> {
  let url = `${this.baseUrl}/movies/`;
  if (search) {
    url += `?search=${encodeURIComponent(search)}`;
  }

  return this.http.get<any[]>(url, this.getOptions()).pipe(
    catchError(this.handleError<any[]>('getMovies'))
  );
}

  // --------------------------------------------------
  //  Get trending movies
  // --------------------------------------------------
  getTrending(): Observable<any[]> {
  // DO NOT attach auth headers for public trending
  return this.http.get<any[]>(`${this.baseUrl}/movies/trending/`)
    .pipe(catchError(this.handleError<any[]>('getTrending')));
}

  // --------------------------------------------------
  //  Search movies
  // --------------------------------------------------
  searchMovies(query: string): Observable<any[]> {
  const url = `${this.baseUrl}/movies/?search=${encodeURIComponent(query)}`;

  return this.http.get<any[]>(url).pipe(
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
  const headers = token ? new HttpHeaders({ Authorization: `Bearer ${token}` }) : undefined;

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
  const token = localStorage.getItem('access_token');

  return this.http.get<any[]>(`${this.baseUrl}/recommendations/`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {}
  });
}
}
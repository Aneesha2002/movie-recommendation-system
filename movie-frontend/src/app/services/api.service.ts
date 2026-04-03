// src/app/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'https://movie-recommendation-system-cef2.onrender.com/api';

  constructor(private http: HttpClient, private authService: AuthService) {}

  /** Helper to include Authorization header if logged in */
  private getAuthHeaders(): HttpHeaders | null {
    const token = this.authService.getAccessToken();
    if (!token) return null;
    return new HttpHeaders({ 'Authorization': `Bearer ${token}` });
  }

  /** Wrap GET requests to return empty array on error */
  private safeGet<T>(obs: Observable<T>): Observable<T | []> {
    return obs.pipe(
      catchError(err => {
        console.error('API error:', err);
        return of([] as any);
      })
    );
  }

  getMovies(): Observable<any[]> {
    const headers = this.getAuthHeaders();
    return this.safeGet(this.http.get<any[]>(`${this.baseUrl}/movies/`, headers ? { headers } : {}));
  }

  getTrending(): Observable<any[]> {
    const headers = this.getAuthHeaders();
    return this.safeGet(this.http.get<any[]>(`${this.baseUrl}/movies/trending/`, headers ? { headers } : {}));
  }

  searchMovies(query: string): Observable<any[]> {
    const headers = this.getAuthHeaders();
    return this.safeGet(this.http.get<any[]>(`${this.baseUrl}/movies/?search=${query}`, headers ? { headers } : {}));
  }

  getMovieById(id: number): Observable<any> {
    const headers = this.getAuthHeaders();
    return this.safeGet(this.http.get<any>(`${this.baseUrl}/movies/${id}/`, headers ? { headers } : {}));
  }

  rateMovie(movieId: number, rating: number): Observable<any> {
    const token = this.authService.getAccessToken();
    if (!token) return of({ error: 'User not logged in' });

    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });
    return this.http.post<any>(`${this.baseUrl}/movies/${movieId}/rate/`, { rating }, { headers });
  }
 getRecommendations(): Observable<any[]> {
  const headers = this.getAuthHeaders();
  return this.safeGet(
    this.http.get<any[]>(
      `${this.baseUrl}/recommendations/`,
      headers ? { headers } : {}
    )
  );
}
}
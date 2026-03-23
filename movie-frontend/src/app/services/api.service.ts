// src/app/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient, private authService: AuthService) {}

  /** Helper to include Authorization header if logged in */
  private getAuthHeaders(): HttpHeaders | null {
    const token = this.authService.getAccessToken();
    if (!token) return null;
    return new HttpHeaders({ 'Authorization': `Bearer ${token}` });
  }

  getMovies(): Observable<any[] | { error: string }> {
  const headers = this.getAuthHeaders();
  if (!headers) return of({ error: 'User not logged in' });
  return this.http.get<any[]>(`${this.baseUrl}/movies/`, { headers });
}

getTrending(): Observable<any[] | { error: string }> {
  const headers = this.getAuthHeaders();
  if (!headers) return of({ error: 'User not logged in' });
  return this.http.get<any[]>(`${this.baseUrl}/movies/trending/`, { headers });
}

searchMovies(query: string): Observable<any[] | { error: string }> {
  const headers = this.getAuthHeaders();
  if (!headers) return of({ error: 'User not logged in' });
  return this.http.get<any[]>(`${this.baseUrl}/movies/?search=${query}`, { headers });
}

  getMovieById(id: number): Observable<any> {
    const headers = this.getAuthHeaders();
    if (!headers) return of({ error: 'User not logged in' });
    return this.http.get(`${this.baseUrl}/movies/${id}/`, { headers });
  }

  /** Submit or update rating with auth header */
  rateMovie(movieId: number, rating: number): Observable<any> {
    const token = this.authService.getAccessToken();
    if (!token) return of({ error: 'User not logged in' });

    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });

    return this.http.post<any>(
      `${this.baseUrl}/movies/${movieId}/rate/`,
      { rating },
      { headers }
    );
  }
}
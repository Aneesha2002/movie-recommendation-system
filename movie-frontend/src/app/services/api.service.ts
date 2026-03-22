// src/app/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getMovies(): Observable<any> {
    return this.http.get(`${this.baseUrl}/movies/`);
  }

  getTrending(): Observable<any> {
    return this.http.get(`${this.baseUrl}/movies/trending/`);
  }

  getMovieById(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/movies/${id}/`);
  }
}
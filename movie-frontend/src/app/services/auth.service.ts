import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/users/';

  constructor(private http: HttpClient) {}

  signup(data: any): Observable<any> {
    return this.http.post(this.apiUrl + 'signup/', data);
  }

  login(data: any): Observable<any> {
  return this.http.post(this.apiUrl + 'login/', data);
}

saveTokens(tokens: any) {
  localStorage.setItem('access_token', tokens.access);
  localStorage.setItem('refresh_token', tokens.refresh);
}

getAccessToken(): string | null {
  return localStorage.getItem('access_token');
}

getRefreshToken(): string | null {
  return localStorage.getItem('refresh_token');
}

  setToken(token: string) {
    localStorage.setItem('token', token);
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }
}
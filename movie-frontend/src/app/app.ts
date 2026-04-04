// src/app/app.ts
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterModule, 
    RouterOutlet,
    HttpClientModule,
    CommonModule
  ],
  template: `
  <h1>Movie App</h1>
  <nav>
    <a routerLink="/login">Login</a> |
    <a routerLink="/signup">Signup</a> |
    <a routerLink="/">Home</a> |
    
    <button *ngIf="isLoggedIn()" (click)="logout()">Logout</button>
  </nav>

  <router-outlet></router-outlet>
  `
})
export class App {

   isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    location.reload(); // refresh UI
  }
}


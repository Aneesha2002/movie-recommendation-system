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
    <a routerLink="/">Home</a> &nbsp;

    <a *ngIf="!isLoggedIn()" routerLink="/login">Login</a>   &nbsp;
    <a *ngIf="!isLoggedIn()" routerLink="/signup">Signup</a> &nbsp;

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
    location.reload();
  }
}
// src/app/app.ts
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { appRoutes } from './app.routes';
import { RouterModule } from '@angular/router';
import { SignupComponent } from './auth/signup/signup';
import { LoginComponent } from './auth/login/login';
import { MoviesComponent } from './movies/movies';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterModule, 
    RouterOutlet,
    SignupComponent,
    LoginComponent,
    MoviesComponent,
    HttpClientModule
  ],
  template: `
    <h1>Movie App</h1>
    <nav>
      <a routerLink="/login">Login</a> |
      <a routerLink="/signup">Signup</a> |
      <a routerLink="/">Home</a>
    </nav>
    <router-outlet></router-outlet>
  `
})
export class App {}
// src/app/app.routes.ts
import { Routes } from '@angular/router';
import { SignupComponent } from './auth/signup/signup';
import { LoginComponent } from './auth/login/login';
import { MoviesComponent } from './movies/movies';

export const appRoutes: Routes = [
  { path: '', component: MoviesComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'login', component: LoginComponent },
  { path: '**', redirectTo: '' } 
];
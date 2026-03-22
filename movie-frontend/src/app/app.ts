import { Component } from '@angular/core';
import { MoviesComponent } from './movies/movies';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MoviesComponent],
  template: `
    <h1>APP WORKING ✅</h1>
    <app-movies></app-movies>
  `
})
export class App {
  constructor() {
    console.log("🔥 APP COMPONENT LOADED");
  }
}
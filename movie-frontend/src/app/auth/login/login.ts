// src/app/auth/login/login.ts
import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
})
export class LoginComponent {
  loginData = { username: '', password: '' };
  message = '';

  constructor(private authService: AuthService, private router: Router) {}

  onLogin(event: Event) {
    event.preventDefault(); // prevents page refresh
    this.authService.login(this.loginData).subscribe({
      next: (res: any) => {
        // store the access token
        this.authService.setToken(res.access);
        this.message = 'Login successful!';
        // navigate to home page (movies)
        this.router.navigate(['/']);
      },
      error: (err: any) => {
        this.message = 'Error: ' + (err.error.detail || 'Login failed');
      },
    });
  }
}
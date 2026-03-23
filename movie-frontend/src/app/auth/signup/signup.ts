// src/app/auth/signup/signup.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './signup.html',
})
export class SignupComponent {
  signupData = { username: '', password: '', password2: '' };
  message = '';

  constructor(private authService: AuthService) {}

  onSignup() {
    this.authService.signup(this.signupData).subscribe({
      next: (res) => (this.message = 'Signup successful! Please login.'),
      error: (err) => (this.message = 'Error: ' + JSON.stringify(err.error)),
    });
  }
}
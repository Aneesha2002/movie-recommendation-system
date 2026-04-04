# 🎬 Movie Recommendation System

A full-stack movie recommendation system built with Django REST Framework (backend) and Angular (frontend).  
Users can browse movies, search, view trending content, rate movies, and receive personalized recommendations.

---

## 🌐 Live Demo

- Frontend (Vercel): https://movie-recommendation-system-git-main-aneesha2002s-projects.vercel.app  
- Backend API (Render): https://movie-recommendation-system-cef2.onrender.com/api  

⚠️ Note: Backend may take 30–60 seconds to respond initially due to cold start on free-tier hosting.

---

## 🚀 Features

### Backend (Django + DRF)
- RESTful APIs for movies, search, ratings, and trending features  
- PostgreSQL database schema for movies, genres, and user ratings  
- JWT-based authentication (signup, login) for protected actions  
- Public access to movie browsing and trending endpoints  
- Personalized recommendation system based on:
  - User’s highly rated genres  
  - Movie average rating  
  - Number of ratings (popularity)  
- Fallback recommendations for new/anonymous users (top-rated + most-rated movies)  
- Integration with TMDb API for movie posters  

---

### Frontend (Angular)
- Browse all movies without login  
- Search movies by title, description, or genre  
- View trending movies  
- Rate movies (only when logged in)  
- Display user’s rating (highlighted stars) after login  
- Personalized recommendations section  
- Conditional UI (login/signup vs logout based on auth state)  

---

## 🛠 Tech Stack

**Backend:**  
- Python 3.10  
- Django 5  
- Django REST Framework  
- PostgreSQL  

**Frontend:**  
- Angular (standalone components)  

**Auth & Tools:**  
- JWT (djangorestframework-simplejwt)  
- TMDb API  
- python-dotenv  

**Deployment:**  
- Backend: Render  
- Frontend: Vercel  

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd movie-recommendation-system
```

---

### 2. Backend Setup

Create `.env` file:

```env
TMDB_API_KEY=your_tmdb_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True
```

Run backend:

```bash
python manage.py migrate
python manage.py runserver
```

(Optional) Load data:

```bash
python manage.py import_movies
python manage.py populate_posters
```

Backend API:
```
http://localhost:8000/api/
```

---

### 3. Frontend Setup

```bash
cd movie_frontend
npm install
ng serve
```

Frontend:
```
http://localhost:4200/
```

⚠️ Make sure backend URL in `api.service.ts` is correct.

---

## 📡 API Endpoints

### Movies
- GET `/api/movies/` → List movies (public)  
- GET `/api/movies/?search=query` → Search movies  
- GET `/api/movies/<id>/` → Movie details  
- GET `/api/movies/trending/` → Trending movies  
- POST `/api/movies/<movie_id>/rate/` → Rate movie (JWT required)  

### Recommendations
- GET `/api/recommendations/` → Personalized or fallback recommendations  

### Users
- POST `/api/users/signup/` → Register  
- POST `/api/users/login/` → Login  

---

## ⚠️ Demo Notes

- Movies and trending are accessible without login  
- Rating requires authentication  
- Recommendations:
  - Logged-in users → personalized  
  - Not logged-in → fallback popular movies  
- Backend may be slow on first request due to free hosting  

---

## 🔮 Future Improvements

- Stronger recommendation system (collaborative filtering)  
- Pagination UI on frontend  
- Add unit & integration tests  
- Improve UI/UX and loading states  
- Production deployment with Nginx + Gunicorn  

---

## 📌 Summary

This project demonstrates:
- Backend API design using Django REST Framework  
- Authentication using JWT  
- Database modeling with relational data (movies, genres, ratings)  
- Recommendation system design (hybrid logic)  
- Full-stack integration and deployment  
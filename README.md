# 🎬 Movie Recommendation System

A full-stack movie recommendation app built with **Django REST Framework** (backend) and **Angular** (frontend).

Users can browse movies, search, rate them, and get personalized recommendations based on their preferences.

---

## Live Demo

* Frontend: https://movie-recommendation-system-git-main-aneesha2002s-projects.vercel.app
* Backend API: https://movie-recommendation-system-cef2.onrender.com/api

⚠️ Note: Backend is hosted on a free tier (Render), so the first request may take ~30–60 seconds.

---

## Features

### Backend

* REST APIs for movies, search, ratings, and recommendations
* JWT authentication (login/signup)
* Public endpoints for browsing and trending
* PostgreSQL database (movies, genres, ratings)

### Recommendation System

* Uses a simple hybrid approach:

  * Genres from movies the user rated highly
  * Average rating of movies
  * Number of ratings (popularity)
* Fallback for new users → top rated / most rated movies
* Already rated movies are excluded

### Frontend

* Browse movies without login
* Search movies (debounced input)
* View trending movies
* Rate movies (only when logged in)
* See your rating instantly reflected
* Personalized recommendations section
* Basic auth-aware UI (login/logout)

---

## Some Design Choices

* Kept backend split into separate apps (`movies`, `users`, `recommendations`) for clarity
* Used Django ORM aggregations (`Avg`, `Count`) instead of raw SQL
* Added caching for trending endpoint to reduce repeated DB queries
* Used `update_or_create` for ratings to avoid duplicates
* Debounced search on frontend to reduce unnecessary API calls
* Recommendation logic kept simple and readable instead of overcomplicating with ML

---

## Performance Notes

* Trending endpoint is cached
* Search input is debounced (300ms)
* Avoids recommending already rated movies
* Queries use aggregation instead of looping in Python

---

## Tech Stack

**Backend**

* Python, Django, Django REST Framework
* PostgreSQL

**Frontend**

* Angular
* RxJS

**Auth & APIs**

* JWT (simplejwt)
* TMDb API (for posters)

**Deployment**

* Backend: Render
* Frontend: Vercel

---

## API Endpoints

### Movies

* `GET /api/movies/` → list movies
* `GET /api/movies/?search=query` → search
* `GET /api/movies/<id>/` → details
* `GET /api/movies/trending/` → trending
* `POST /api/movies/<id>/rate/` → rate (auth required)

### Recommendations

* `GET /api/recommendations/`

### Users

* `POST /api/users/signup/`
* `POST /api/users/login/`

---

## Local Setup

### Backend

```bash
git clone <repo-url>
cd movie-recommendation-system

# create .env
TMDB_API_KEY=your_key
SECRET_KEY=your_secret
DEBUG=True

python manage.py migrate
python manage.py runserver
```

(Optional)

```bash
python manage.py import_movies
python manage.py populate_posters
```

---

### Frontend

```bash
cd movie_frontend
npm install
ng serve
```

---

## Future Improvements

* Move recommendation logic to background jobs (Celery)
* Add Redis caching for recommendations
* Improve recommendation quality (collaborative filtering)
* Add tests
* Better UI/UX

---

## Summary

This project mainly focuses on:

* building REST APIs with Django
* handling relational data (movies, genres, ratings)
* implementing a simple recommendation system
* integrating frontend with backend
* deploying a full-stack app

---
# 🎬 Movie Recommendation System

A **movie recommendation system** built with **Django REST Framework** for the backend and **Angular** for the frontend.  
Features include movie browsing, searching, ratings, trending movies, and personalized recommendations.

---

## 🚀 Features

### Backend (Django + DRF)
- **Movie management** with genres, ratings, and average rating calculations  
- **User authentication** via JWT (signup, login, token refresh)  
- **Personalized recommendations** based on user ratings  
- **Trending movies** endpoint (most rated & highest-rated)  
- **External API integration** with [TMDb](https://www.themoviedb.org/) for movie posters  
- **Caching** using Redis (for trending & movie list endpoints)  
- **CSV import commands** for initial movie data  

### Frontend (Angular)
- Responsive UI to display movies and trending list  
- **Search** movies by title, description, or genre  
- **Rate movies** and see your rating alongside the average rating  
- Displays **3 recommendations per movie**  

---

## 🛠 Tech Stack

- **Backend:** Python 3.10, Django 5.2, Django REST Framework, PostgreSQL, Redis  
- **Frontend:** Angular 17 (standalone components)  
- **DevOps:** Docker, Docker Compose  
- **Libraries & Tools:** `djangorestframework-simplejwt`, `django-redis`, `rapidfuzz`, `requests`, `python-dotenv`

---

## ⚙️ Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd movie-recommendation-system

2. Backend Setup
Create .env file:
TMDB_API_KEY=your_tmdb_api_key
SECRET_KEY=your_django_secret_key
DEBUG=True
Build and run Docker containers:
docker-compose up --build
Apply migrations & import movies:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py import_movies
docker-compose exec web python manage.py populate_posters

Backend API is available at: http://localhost:8000/api/

3. Frontend Setup
Navigate to frontend folder:
cd movie_frontend
Install dependencies:
npm install
Run Angular app:
ng serve

Frontend is accessible at: http://localhost:4200/

⚠️ Ensure backend is running at http://localhost:8000/ or update baseUrl in api.service.ts.

 API Endpoints
Endpoint	Method	Description
/api/movies/	GET	List all movies (supports search ?search=)
/api/movies/<id>/	GET	Retrieve movie details with recommendations
/api/movies/trending/	GET	Top 5 trending movies
/api/movies/<id>/rate/	POST	Submit or update rating (JWT required)
/api/users/signup/	POST	Register new user
/api/users/login/	POST	JWT login

 Future Improvements
Frontend pagination for movies
Improved recommendation algorithm: hybrid collaborative + content-based filtering
Unit & integration tests for backend endpoints
Production-ready deployment: Nginx + Gunicorn, HTTPS, Docker optimizations
Cloud media storage for posters (e.g., S3 or Cloudinary)
Rate limiting and caching enhancements for high traffic

 Notes
The system currently displays 3 recommendations per movie.
Redis caching is used for trending movies and movie list endpoints; suitable for demo purposes but can be scaled for production.
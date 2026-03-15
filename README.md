# Movie Recommendation Backend Service

## Overview

This project is a backend service that provides personalized movie recommendations based on user ratings, genre similarity, and movie popularity. Users can browse movies, rate them, and receive recommendations tailored to their preferences.

The system is designed as a containerized backend application built with Django and Django REST Framework, using PostgreSQL as the primary database.

---

## Features

* User authentication (signup and login)
* Movie catalog with genres and metadata
* User rating system (1–5 stars)
* Hybrid recommendation engine based on:

  * Genre similarity
  * User rating history
  * Movie popularity
* Search movies by title
* Filter movies by genre
* Trending / popular movies endpoint
* REST API for movies, ratings, and recommendations
* Simple frontend using Django templates
* Containerized environment using Docker
* Optional Redis caching layer

---

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Docker
* Redis (optional)

---

## Architecture

```
Client (Browser / API client)
        |
        v
Django REST API
        |
        v
PostgreSQL Database
        |
        v
Redis Cache (optional)
```

---

## Project Structure

```
movie-recommendation-service/

├── app/
│   ├── manage.py
│   ├── config/
│   ├── users/
│   ├── movies/
│   ├── ratings/
│   └── recommendations/
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── requirements.txt
└── README.md
```

---

## Core API Endpoints

```
POST   /api/auth/signup
POST   /api/auth/login

GET    /api/movies
GET    /api/movies/{id}

POST   /api/ratings

GET    /api/movies/trending
GET    /api/recommendations
```

---

## Recommendation Strategy

The recommendation system uses a hybrid scoring approach that combines multiple factors.

Example scoring formula:

```
Recommendation Score =
0.5 * Genre Similarity
+ 0.3 * User Rating Similarity
+ 0.2 * Movie Popularity
```

The system recommends movies that:

* Match the genres the user rates highly
* Are popular or highly rated by other users
* Have not already been rated by the user

---

## Setup (Planned)

Instructions for running the project will include:

```
git clone <repository>
docker compose up
python manage.py migrate
python manage.py runserver
```

---

## Future Improvements

* Advanced recommendation algorithms
* Collaborative filtering
* Background recommendation jobs
* Pagination and performance optimization
* Unit and integration tests

---

## Goal of the Project

This project demonstrates backend engineering skills including:

* REST API design
* relational database modeling
* recommendation logic
* containerized development with Docker
* scalable backend architecture

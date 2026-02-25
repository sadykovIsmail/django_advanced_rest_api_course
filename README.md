# Django Advanced REST API Course

A hands-on learning repository by **Ismail Sadykov** covering advanced Django REST Framework concepts through three progressively more complex API projects — from a simple SQLite-backed Todo API to a fully Dockerized Blog API with JWT authentication, image uploads, and Swagger documentation.

---

## Table of Contents

- [Projects Overview](#projects-overview)
- [Tech Stack](#tech-stack)
- [Project 1: Todo App API](#project-1-todo-app-api)
- [Project 2: Notes App API](#project-2-notes-app-api)
- [Project 3: Blog App API](#project-3-blog-app-api)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [License](#license)

---

## Projects Overview

| # | Project | Database | Auth | Docker | Image Upload | API Docs |
|---|---------|----------|------|--------|--------------|----------|
| 1 | Todo App API | SQLite | Token Auth | No | No | No |
| 2 | Notes App API | PostgreSQL | JWT | Yes | No | Swagger UI |
| 3 | Blog App API | PostgreSQL | JWT | Yes | Yes | Swagger UI |

Each project builds on the previous one, introducing new concepts and production-ready patterns.

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.10 – 3.12 |
| Framework | Django 3.2 / 5.2 |
| REST API | Django REST Framework 3.16 |
| Authentication | Token Auth (Project 1), SimpleJWT (Projects 2 & 3) |
| Database | SQLite (Project 1), PostgreSQL 16 (Projects 2 & 3) |
| Containerization | Docker, Docker Compose |
| Web Server | Nginx (Alpine), Gunicorn |
| Image Processing | Pillow |
| API Documentation | drf-spectacular (OpenAPI 3 / Swagger UI) |
| Static Files | WhiteNoise (Project 3) |
| Config Management | python-dotenv |

---

## Project 1: Todo App API

**Location:** `1. todo_app_api/`

A foundational REST API for task management using SQLite and Django's built-in token authentication. This project establishes core DRF patterns — models, serializers, viewsets, and routers — with per-user data isolation.

### Features

- Full CRUD for tasks via `ModelViewSet`
- Token-based authentication (`rest_framework.authtoken`)
- Per-user task isolation (users only see their own tasks)
- Input validation: `quantity` field restricted to values 1–5
- Read-only fields: `id`, `created_at`, `completed`, `user`

### Data Model

**Task**

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField | Primary key |
| `title` | CharField(255) | Required |
| `description` | TextField | Optional |
| `completed` | BooleanField | Default: `False`, read-only |
| `quantity` | IntegerField | 1–5, default: `1` |
| `created_at` | DateTimeField | Auto-set on create |
| `user` | ForeignKey (User) | Auto-assigned, read-only |

### Running Locally

```bash
cd "1. todo_app_api"
python -m venv venv && source venv/bin/activate
pip install django djangorestframework
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tasks/` | List all tasks for authenticated user |
| `POST` | `/api/tasks/` | Create a new task |
| `GET` | `/api/tasks/{id}/` | Retrieve a specific task |
| `PUT` | `/api/tasks/{id}/` | Update a task |
| `PATCH` | `/api/tasks/{id}/` | Partially update a task |
| `DELETE` | `/api/tasks/{id}/` | Delete a task |

**Authentication:** Include a token in the `Authorization` header:
```
Authorization: Token <your-token>
```

---

## Project 2: Notes App API

**Location:** `2. notes_app_api/`

An upgraded notes management API running in Docker with PostgreSQL, JWT authentication, Nginx reverse proxy, and auto-generated Swagger documentation.

### Features

- Full CRUD for notes, categories, and tags
- Many-to-many relationship between Notes and Tags
- JWT authentication via `djangorestframework-simplejwt`
  - Access token lifetime: 1 hour
  - Refresh token lifetime: 7 days
- PostgreSQL 16 database
- Dockerized with `docker-compose` (Django + PostgreSQL + Nginx)
- Nginx as a reverse proxy serving static/media files
- Interactive Swagger UI via `drf-spectacular`
- Auto-migration and `collectstatic` on container startup

### Data Models

**Category**

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField | Primary key |
| `name` | CharField(255) | Required |
| `created_at` | DateTimeField | Auto-set |
| `updated_at` | DateTimeField | Auto-updated |

**Tag**

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField | Primary key |
| `name` | CharField(255) | Required |

**Note**

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField | Primary key |
| `title` | CharField(255) | Required |
| `content` | TextField | Optional |
| `user` | ForeignKey (User) | Auto-assigned |
| `tags` | ManyToManyField (Tag) | Multiple tags |
| `category` | ForeignKey (Category) | Required |
| `created_at` | DateTimeField | Auto-set |
| `updated_at` | DateTimeField | Auto-updated |

### Running with Docker

```bash
cd "2. notes_app_api"
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### API Endpoints

**Authentication**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/token/` | Obtain JWT access & refresh tokens |
| `POST` | `/api/refresh/` | Refresh access token |

**Notes**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/notes/` | List notes (current user only) |
| `POST` | `/api/notes/` | Create a note |
| `GET` | `/api/notes/{id}/` | Retrieve a note |
| `PUT` | `/api/notes/{id}/` | Update a note |
| `PATCH` | `/api/notes/{id}/` | Partially update a note |
| `DELETE` | `/api/notes/{id}/` | Delete a note |

**Categories & Tags**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET/POST` | `/api/categories/` | List or create categories |
| `GET/PUT/PATCH/DELETE` | `/api/categories/{id}/` | Manage a category |
| `GET/POST` | `/api/tags/` | List or create tags |
| `GET/PUT/PATCH/DELETE` | `/api/tags/{id}/` | Manage a tag |

**Documentation**

| Endpoint | Description |
|----------|-------------|
| `/api/docs/` | Interactive Swagger UI |
| `/api/schema/` | Raw OpenAPI schema (JSON/YAML) |

**Authentication:** Include the JWT access token in the `Authorization` header:
```
Authorization: Bearer <access-token>
```

---

## Project 3: Blog App API

**Location:** `3. blog_app_api/`

The most feature-complete project — a full blog platform API with author profiles, blog posts, image upload support, custom object-level permissions, and production-style Docker deployment.

### Features

- Full CRUD for authors and blog posts
- JWT authentication via `djangorestframework-simplejwt`
- **Image upload** for blog post cover images (Pillow + `MultiPartParser`)
- Custom `IsOwner` permission (object-level authorization)
- Per-user data scoping for both authors and posts
- PostgreSQL 16 database
- Dockerized with `docker-compose` (Django + PostgreSQL + Nginx)
- Nginx reverse proxy with static and media file serving
- WhiteNoise for static file handling
- Interactive Swagger UI via `drf-spectacular`
- `.env` file-based configuration management

### Data Models

**AuthorModel**

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField | Primary key |
| `name` | CharField(255) | Required |
| `email` | EmailField(255) | Required |
| `created_at` | DateTimeField | Auto-set |
| `user` | ForeignKey (User) | Auto-assigned |

**BlogPostModel**

| Field | Type | Notes |
|-------|------|-------|
| `id` | AutoField | Primary key |
| `title` | CharField(255) | Required |
| `content` | TextField | Required |
| `author` | ForeignKey (AuthorModel) | Required |
| `image` | ImageField | Optional, stored under `posts/` |
| `created_at` | DateTimeField | Auto-set |
| `updated_at` | DateTimeField | Auto-updated |
| `user` | ForeignKey (User) | Auto-assigned |

### Running with Docker

1. The `.env` file is already present in `3. blog_app_api/`. For production, update it with secure values:

```env
DEBUG=0
SECRET_KEY=your-secure-secret-key-here

POSTGRES_DB=blog_db
POSTGRES_USER=blog_user
POSTGRES_PASSWORD=blog_password

DB_HOST=db
DB_PORT=5432
```

2. Start the stack:

```bash
cd "3. blog_app_api"
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### API Endpoints

**Authentication**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/token/` | Obtain JWT access & refresh tokens |
| `POST` | `/api/token/refresh/` | Refresh access token |

**Authors**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/author/` | List authors (current user only) |
| `POST` | `/api/author/` | Create an author profile |
| `GET` | `/api/author/{id}/` | Retrieve an author |
| `PUT` | `/api/author/{id}/` | Update an author |
| `PATCH` | `/api/author/{id}/` | Partially update an author |
| `DELETE` | `/api/author/{id}/` | Delete an author |

**Blog Posts**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/posts/` | List posts (current user only) |
| `POST` | `/api/posts/` | Create a blog post |
| `GET` | `/api/posts/{id}/` | Retrieve a post |
| `PUT` | `/api/posts/{id}/` | Update a post |
| `PATCH` | `/api/posts/{id}/` | Partially update a post |
| `DELETE` | `/api/posts/{id}/` | Delete a post |
| `POST` | `/api/posts/{id}/upload-image/` | Upload a cover image for a post |

**Documentation**

| Endpoint | Description |
|----------|-------------|
| `/api/docs/` | Interactive Swagger UI |
| `/api/schema/` | Raw OpenAPI schema (JSON/YAML) |

**Authentication:** Include the JWT access token in the `Authorization` header:
```
Authorization: Bearer <access-token>
```

### Image Upload Example

```bash
curl -X POST http://localhost:8000/api/posts/1/upload-image/ \
  -H "Authorization: Bearer <access-token>" \
  -F "image=@/path/to/image.jpg"
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (for Projects 2 & 3)
- Git

### Clone the Repository

```bash
git clone https://github.com/sadykovIsmail/django_advanced_rest_api_course.git
cd django_advanced_rest_api_course
```

### Project 1 — Quick Start (No Docker)

```bash
cd "1. todo_app_api"
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install django djangorestframework
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# API available at http://127.0.0.1:8000
```

### Projects 2 & 3 — Docker Quick Start

```bash
# Notes App
cd "2. notes_app_api"
docker-compose up --build

# Blog App
cd "3. blog_app_api"
docker-compose up --build
```

Once running, create a superuser to start using the API:

```bash
# In a separate terminal, exec into the web container
docker-compose exec web python manage.py createsuperuser
```

---

## API Reference

### Obtaining a JWT Token (Projects 2 & 3)

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Using the Access Token

```bash
curl http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer <access-token>"
```

### Refreshing the Token

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh-token>"}'
```

### Obtaining a Token (Project 1 — Token Auth)

Use the Django admin panel at `http://127.0.0.1:8000/admin/` to generate a token under **Auth Token → Tokens**, or via the DRF browsable API.

---

## Environment Variables

Projects 2 and 3 are configured via environment variables. Create or update a `.env` file in the respective project directory:

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Debug mode (`1` = on, `0` = off) | `0` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `POSTGRES_DB` | PostgreSQL database name | `blog_db` |
| `POSTGRES_USER` | PostgreSQL username | `blog_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `blog_password` |
| `DB_HOST` | Database host (Docker service name) | `db` |
| `DB_PORT` | Database port | `5432` |

> **Security note:** Never commit `.env` files with real credentials. Both Projects 2 and 3 include `.gitignore` entries for `.env`.

---

## Project Structure

```
django_advanced_rest_api_course/
├── 1. todo_app_api/                 # Project 1: SQLite + Token Auth
│   ├── core/                        # Django settings, URLs, WSGI
│   ├── tasks/                       # Tasks app
│   │   ├── models.py                # Task model
│   │   ├── serializers.py           # TaskSerializer
│   │   ├── views.py                 # TaskViewSet
│   │   ├── urls.py                  # Router registration
│   │   └── migrations/
│   └── manage.py
│
├── 2. notes_app_api/                # Project 2: PostgreSQL + JWT + Docker
│   ├── app/
│   │   ├── core/                    # Django settings, URLs, WSGI
│   │   ├── notes/                   # Notes app (Note, Category, Tag)
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   ├── manage.py
│   │   └── requirements.txt
│   ├── docker/
│   │   └── nginx/
│   │       └── default.conf         # Nginx reverse proxy config
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── 3. blog_app_api/                 # Project 3: Blog + Image Upload
│   ├── app/
│   │   ├── core/                    # Django settings, URLs, WSGI
│   │   ├── author/                  # Author & BlogPost app
│   │   │   ├── models.py            # AuthorModel, BlogPostModel
│   │   │   ├── serializers.py       # Author, BlogPost, PostImage serializers
│   │   │   ├── views.py             # ViewSets + IsOwner permission
│   │   │   ├── urls.py
│   │   │   └── migrations/
│   │   ├── manage.py
│   │   └── requirements.txt
│   ├── docker/
│   │   └── nginx/
│   │       └── default.conf
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env                         # Environment variables (not committed)
│
├── roadmap.txt
├── LICENSE
└── README.md
```

---

## Roadmap

| Week | Goals | Status |
|------|-------|--------|
| Week 1 | Convert Todo app to PostgreSQL | Done (Project 2) |
| Week 1 | Dockerize the app | Done (Projects 2 & 3) |
| Week 2 | Add image upload | Done (Project 3) |
| Week 2 | Write 10+ API tests | Planned |
| Week 2 | Add GitHub Actions CI/CD | Planned |

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

*Built with Django REST Framework while learning advanced backend development patterns.*

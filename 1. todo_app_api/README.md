<div align="center">

# Todo App API

### Project 1 of 3 — Django REST Framework Foundations

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-ff1709?style=flat-square)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

**A clean, authenticated REST API for task management — built to master Django REST Framework fundamentals: models, serializers, viewsets, routers, and token authentication.**

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Folder Structure](#folder-structure)
- [Data Model](#data-model)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Installation](#installation)
- [Example Requests](#example-requests)
- [Example Responses](#example-responses)
- [Future Improvements](#future-improvements)

---

## Overview

The Todo App API is a foundational REST API project that demonstrates the core building blocks of Django REST Framework. It provides a fully authenticated CRUD interface for managing personal tasks, with per-user data isolation ensuring users only ever see and manage their own tasks.

This project deliberately keeps the infrastructure simple (no Docker, SQLite database) so the focus stays entirely on DRF patterns.

**What this project practices:**
- Defining Django models with validators and relationships
- Building serializers with computed read-only fields
- Using `ModelViewSet` for automatic CRUD endpoint generation
- Registering routes via `DefaultRouter`
- Securing endpoints with `TokenAuthentication` and `IsAuthenticated`
- Overriding `get_queryset()` and `perform_create()` for user-scoped data

---

## Features

- Full **CRUD** task management (Create, Read, Update, Delete)
- **Token authentication** — every endpoint is protected, unauthorized requests return `401`
- **Per-user data isolation** — `get_queryset()` filters tasks to the authenticated user
- **Input validation** — `quantity` field is validated at the model level using Django's `MinValueValidator` and `MaxValueValidator` (allowed range: 1–5)
- **Read-only field enforcement** — `id`, `created_at`, `completed`, and `user` cannot be set by the client
- **User display field** — serializer exposes `user_name` (read-only) alongside the `user` FK id

---

## Project Architecture

```mermaid
graph TD
    Client(["HTTP Client<br/>(curl / Postman)"])
    Router["DefaultRouter<br/>/api/tasks/"]
    ViewSet["TaskViewSet<br/>(ModelViewSet)"]
    Auth["TokenAuthentication<br/>+ IsAuthenticated"]
    Serializer["TaskSerializer<br/>(ModelSerializer)"]
    Model["Task Model"]
    DB[("SQLite\ndb.sqlite3")]

    Client -->|"Token in header"| Router
    Router --> Auth
    Auth -->|"Authenticated"| ViewSet
    ViewSet --> Serializer
    Serializer --> Model
    Model --> DB
```

### Request Lifecycle

```mermaid
sequenceDiagram
    actor Client
    participant Router
    participant Auth as Token Auth Middleware
    participant ViewSet as TaskViewSet
    participant DB as SQLite

    Client->>Router: GET /api/tasks/<br/>Authorization: Token abc123
    Router->>Auth: Validate token
    Auth->>DB: Lookup token → user
    DB-->>Auth: User object
    Auth-->>ViewSet: request.user = User(id=1)
    ViewSet->>DB: Task.objects.filter(user=request.user)
    DB-->>ViewSet: [Task, Task, ...]
    ViewSet-->>Client: 200 OK JSON array
```

---

## Folder Structure

```
1. todo_app_api/
├── core/
│   ├── __init__.py
│   ├── settings.py          # Project settings: SQLite, REST_FRAMEWORK config
│   ├── urls.py              # Root URL config — includes tasks.urls
│   ├── wsgi.py
│   └── asgi.py
├── tasks/
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py            # Task model definition + validators
│   ├── serializers.py       # TaskSerializer with user_name field
│   ├── views.py             # TaskViewSet: get_queryset, perform_create
│   ├── urls.py              # DefaultRouter — registers TaskViewSet
│   ├── tests.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── db.sqlite3
└── manage.py
```

---

## Data Model

### Task

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string password
    }
    TASK {
        int id PK
        string title
        text description
        bool completed
        int quantity
        datetime created_at
        int user_id FK
    }
    USER ||--o{ TASK : "owns"
```

| Field | Type | Constraints | Default | Notes |
|-------|------|-------------|---------|-------|
| `id` | `AutoField` | Primary Key | — | Auto-generated, read-only |
| `title` | `CharField(255)` | Required | — | Task name |
| `description` | `TextField` | Optional | `""` | Task details |
| `completed` | `BooleanField` | — | `False` | Read-only via serializer |
| `quantity` | `IntegerField` | Min: 1, Max: 5 | `1` | Validated at model level |
| `created_at` | `DateTimeField` | `auto_now_add=True` | — | Set on creation, read-only |
| `user` | `ForeignKey(User)` | `CASCADE` | — | Auto-assigned, read-only |

---

## API Endpoints

**Base URL:** `http://127.0.0.1:8000`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| `GET` | `/api/tasks/` | List all tasks for the authenticated user | Yes |
| `POST` | `/api/tasks/` | Create a new task | Yes |
| `GET` | `/api/tasks/{id}/` | Retrieve a specific task | Yes |
| `PUT` | `/api/tasks/{id}/` | Full update of a task | Yes |
| `PATCH` | `/api/tasks/{id}/` | Partial update of a task | Yes |
| `DELETE` | `/api/tasks/{id}/` | Delete a task | Yes |

> All endpoints require an `Authorization: Token <token>` header. Requests without a valid token receive a `401 Unauthorized` response.

---

## Authentication

This project uses Django REST Framework's built-in **Token Authentication**.

### How it works

1. Each user has a unique, randomly-generated token stored in the `authtoken_token` database table
2. The client sends this token in the `Authorization` header with every request
3. DRF validates the token, looks up the associated user, and sets `request.user`

### Obtaining a Token

**Via Django Admin:**
1. Go to `http://127.0.0.1:8000/admin/`
2. Log in with your superuser credentials
3. Navigate to **Auth Token → Tokens → Add Token**
4. Select the user and save — copy the generated token

**Via DRF Browsable API:**
Visit `http://127.0.0.1:8000/api/tasks/` in a browser and use the login button.

### Using the Token

```bash
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4
```

---

## Installation

### Requirements

- Python 3.10+
- pip

No Docker required for this project.

### Steps

```bash
# 1. Navigate to the project directory
cd "1. todo_app_api"

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

# 4. Install dependencies
pip install django djangorestframework

# 5. Apply migrations (creates db.sqlite3)
python manage.py migrate

# 6. Create a superuser account
python manage.py createsuperuser
# Follow the prompts: username, email, password

# 7. Start the development server
python manage.py runserver
```

The API is now live at `http://127.0.0.1:8000`.

Next, generate an auth token via the admin panel at `http://127.0.0.1:8000/admin/`.

---

## Example Requests

### List Tasks

```bash
curl http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4"
```

### Create a Task

```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Read DRF documentation",
    "description": "Cover serializers and viewsets chapters",
    "quantity": 2
  }'
```

### Retrieve a Single Task

```bash
curl http://127.0.0.1:8000/api/tasks/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4"
```

### Update a Task (Partial)

```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 5}'
```

### Delete a Task

```bash
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4"
```

---

## Example Responses

### `GET /api/tasks/` — 200 OK

```json
[
  {
    "id": 1,
    "title": "Read DRF documentation",
    "description": "Cover serializers and viewsets chapters",
    "quantity": 2,
    "completed": false,
    "created_at": "2024-01-15T10:30:00.123456Z",
    "user": 1,
    "user_name": "admin"
  },
  {
    "id": 2,
    "title": "Build a REST API",
    "description": "",
    "quantity": 1,
    "completed": false,
    "created_at": "2024-01-15T11:00:00.000000Z",
    "user": 1,
    "user_name": "admin"
  }
]
```

### `POST /api/tasks/` — 201 Created

```json
{
  "id": 3,
  "title": "Read DRF documentation",
  "description": "Cover serializers and viewsets chapters",
  "quantity": 2,
  "completed": false,
  "created_at": "2024-01-15T12:00:00.000000Z",
  "user": 1,
  "user_name": "admin"
}
```

### `POST /api/tasks/` — 400 Bad Request (invalid quantity)

```json
{
  "quantity": [
    "Ensure this value is less than or equal to 5."
  ]
}
```

### `GET /api/tasks/` — 401 Unauthorized (missing token)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Future Improvements

- [ ] Migrate from SQLite to PostgreSQL for production readiness
- [ ] Dockerize with Docker Compose
- [ ] Add a `PATCH /api/tasks/{id}/complete/` action to toggle completion status
- [ ] Add pagination (`PageNumberPagination`) to the list endpoint
- [ ] Add filtering and ordering (`django-filter`) — by `completed`, `created_at`, etc.
- [ ] Write automated tests (unit + integration) using `APITestCase`
- [ ] Add GitHub Actions CI to run tests on every push
- [ ] Add user registration and token-obtain endpoints (currently requires admin panel)

---

<div align="center">

Part of the **[Django Advanced REST API Course](../README.md)** repository

</div>

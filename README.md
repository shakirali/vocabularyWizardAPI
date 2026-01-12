# Vocabulary Wizard API

FastAPI backend for the Vocabulary iOS application. This API provides RESTful endpoints for vocabulary management, quiz generation, progress tracking, and user authentication.

## Features

- **User Authentication**: JWT-based authentication with refresh tokens
- **Vocabulary Management**: CRUD operations for vocabulary items organized by year groups
- **Progress Tracking**: Track user progress, mastered words, and practice sessions
- **Quiz Generation**: Generate quizzes from mastered vocabulary words
- **Sentence Fill-in-the-Blank**: Generate sentence completion questions
- **Flashcards**: Paginated flashcard endpoints for vocabulary review

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL 14+ (or SQLite for development)
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose, passlib)
- **Validation**: Pydantic v2

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection & session
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies (auth, db session)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py         # Authentication routes
│   │       ├── vocabulary.py   # Vocabulary routes
│   │       ├── progress.py     # Progress routes
│   │       ├── quiz.py         # Quiz routes
│   │       ├── sentences.py    # Sentence fill routes
│   │       └── flashcards.py   # Flashcard routes
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT, password hashing
│   │   ├── config.py           # Settings (Pydantic)
│   │   └── exceptions.py       # Custom exceptions
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User SQLAlchemy model
│   │   ├── vocabulary.py       # VocabularyItem model
│   │   ├── progress.py         # UserProgress model
│   │   └── quiz.py             # QuizQuestion, SentenceQuestion models
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   │   ├── vocabulary.py       # VocabularyItem schemas
│   │   ├── progress.py         # Progress schemas
│   │   ├── quiz.py             # Quiz schemas
│   │   └── common.py           # Common schemas (pagination, etc.)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── vocabulary_service.py
│   │   ├── progress_service.py
│   │   └── quiz_service.py     # Quiz generation logic
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py             # Base repository pattern
│   │   ├── user_repository.py
│   │   ├── vocabulary_repository.py
│   │   └── progress_repository.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── quiz_generator.py   # Quiz question generation algorithms
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   └── ...
│
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL 14+ (optional, SQLite works for development)
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd vocabularyWizardAPI
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Update `.env` with your configuration (especially `SECRET_KEY` and `DATABASE_URL`).

6. Initialize the database:
```bash
# The database tables will be created automatically on first run
# Or use Alembic for migrations:
# alembic init alembic
# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head
```

7. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Docker Setup

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

This will start:
- PostgreSQL database on port 5432
- FastAPI application on port 8000

2. Access the API:
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - Logout (client-side token removal)

### Year Groups
- `GET /api/v1/years` - Get all available year groups

### Vocabulary
- `GET /api/v1/vocabulary` - Get vocabulary items (with filters)
- `GET /api/v1/vocabulary/{id}` - Get specific vocabulary item
- `POST /api/v1/vocabulary` - Create vocabulary item (admin)
- `PUT /api/v1/vocabulary/{id}` - Update vocabulary item (admin)
- `DELETE /api/v1/vocabulary/{id}` - Delete vocabulary item (admin)

### Progress
- `GET /api/v1/progress` - Get user's progress summary
- `GET /api/v1/progress/mastered` - Get mastered word IDs for a year
- `POST /api/v1/progress/mastered` - Mark word as mastered
- `DELETE /api/v1/progress/mastered/{id}` - Unmark word as mastered
- `POST /api/v1/progress/practice` - Record practice session

### Quiz
- `POST /api/v1/quiz/generate` - Generate quiz from mastered words
- `POST /api/v1/quiz/submit` - Submit quiz answers

### Sentences
- `POST /api/v1/sentences/generate` - Generate sentence fill questions
- `POST /api/v1/sentences/submit` - Submit sentence answers

### Flashcards
- `GET /api/v1/flashcards` - Get flashcards for a year (paginated)

## Testing

Run tests with pytest:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Development

### Code Quality

Format code with black:
```bash
black app/
```

Sort imports with isort:
```bash
isort app/
```

Lint with flake8:
```bash
flake8 app/
```

Type check with mypy:
```bash
mypy app/
```

## Environment Variables

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key (change in production!)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiration (default: 60)
- `REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiration (default: 7)
- `CORS_ORIGINS` - Allowed CORS origins (JSON array)
- `ENVIRONMENT` - Environment (dev/staging/production)

## License

[Your License Here]

## Contributing

[Contributing guidelines]


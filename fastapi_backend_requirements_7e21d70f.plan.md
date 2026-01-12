---
name: FastAPI Backend Requirements
overview: Create a comprehensive requirements.md file for a FastAPI backend that mirrors the iOS app's functionality, including vocabulary management, quiz generation, progress tracking, and user authentication.
todos: []
---

# FastAPI Backend Requirements Document

## Overview

This document specifies the requirements for building a FastAPI backend to support the Vocabulary iOS application. The backend will provide RESTful APIs for vocabulary management, quiz generation, progress tracking, and user authentication.

## 1. Core Data Models

### 1.1 VocabularyItem

- **Fields:**
  - `id`: UUID (primary key)
  - `year`: YearGroup enum (Year 3, Year 4, Year 5, Year 6)
  - `word`: String (required, unique per year)
  - `meaning`: String (required)
  - `antonyms`: List[String]
  - `exampleSentences`: List[String]
  - `created_at`: DateTime
  - `updated_at`: DateTime

### 1.2 YearGroup

- Enum values: `year3`, `year4`, `year5`, `year6`
- Each has: `display_name`, `short_code` (Y3, Y4, Y5, Y6)

### 1.3 QuizQuestion

- **Fields:**
  - `id`: UUID
  - `vocabulary_item_id`: UUID (foreign key)
  - `prompt`: String (the word to define)
  - `options`: List[String] (multiple choice options)
  - `correct_index`: Integer (0-based index of correct answer)
  - `type`: Enum (currently only "meaning")
  - `created_at`: DateTime

### 1.4 SentenceQuestion

- **Fields:**
  - `id`: UUID
  - `sentence_template`: String (sentence with {word} placeholder)
  - `correct_word`: String
  - `options`: List[String] (multiple choice options)
  - `vocabulary_item_id`: UUID (foreign key)
  - `created_at`: DateTime

### 1.5 User

- **Fields:**
  - `id`: UUID (primary key)
  - `username`: String (unique, required)
  - `email`: String (unique, required, validated)
  - `password_hash`: String (hashed, never exposed)
  - `full_name`: String (optional)
  - `created_at`: DateTime
  - `updated_at`: DateTime
  - `is_active`: Boolean (default: True)

### 1.6 UserProgress

- **Fields:**
  - `id`: UUID (primary key)
  - `user_id`: UUID (foreign key)
  - `vocabulary_item_id`: UUID (foreign key)
  - `year_group`: YearGroup enum
  - `is_mastered`: Boolean (default: False)
  - `mastered_at`: DateTime (nullable)
  - `times_practiced`: Integer (default: 0)
  - `last_practiced_at`: DateTime (nullable)
  - `created_at`: DateTime
  - `updated_at`: DateTime
  - **Unique constraint:** (user_id, vocabulary_item_id)

## 2. API Endpoints

### 2.1 Authentication Endpoints

#### POST `/api/v1/auth/register`

- **Description:** Register a new user
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "full_name": "string (optional)"
  }
  ```

- **Response:** 201 Created
  ```json
  {
    "id": "uuid",
    "username": "string",
    "email": "string",
    "full_name": "string",
    "created_at": "datetime"
  }
  ```


#### POST `/api/v1/auth/login`

- **Description:** Authenticate user and return JWT token
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

- **Response:** 200 OK
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "expires_in": 3600,
    "user": {
      "id": "uuid",
      "username": "string",
      "email": "string"
    }
  }
  ```


#### POST `/api/v1/auth/refresh`

- **Description:** Refresh access token using refresh token
- **Headers:** Authorization: Bearer {refresh_token}
- **Response:** 200 OK (same as login)

#### POST `/api/v1/auth/logout`

- **Description:** Logout user (invalidate token)
- **Headers:** Authorization: Bearer {token}
- **Response:** 200 OK

### 2.2 Year Group Endpoints

#### GET `/api/v1/years`

- **Description:** Get all available year groups
- **Authentication:** Optional (public endpoint)
- **Response:** 200 OK
  ```json
  [
    {
      "value": "year3",
      "display_name": "Year 3",
      "short_code": "Y3"
    }
  ]
  ```


### 2.3 Vocabulary Item Endpoints

#### GET `/api/v1/vocabulary`

- **Description:** Get vocabulary items with optional filters
- **Authentication:** Required
- **Query Parameters:**
  - `year`: YearGroup (optional, filter by year)
  - `skip`: Integer (default: 0, pagination)
  - `limit`: Integer (default: 100, pagination)
  - `search`: String (optional, search word/meaning)
- **Response:** 200 OK
  ```json
  {
    "items": [
      {
        "id": "uuid",
        "year": "year3",
        "word": "string",
        "meaning": "string",
        "antonyms": ["string"],
        "example_sentences": ["string"]
      }
    ],
    "total": 100,
    "skip": 0,
    "limit": 100
  }
  ```


#### GET `/api/v1/vocabulary/{vocabulary_id}`

- **Description:** Get a specific vocabulary item by ID
- **Authentication:** Required
- **Response:** 200 OK (single VocabularyItem object)

#### POST `/api/v1/vocabulary`

- **Description:** Create a new vocabulary item (admin only)
- **Authentication:** Required (admin role)
- **Request Body:** VocabularyItem (without id, created_at, updated_at)
- **Response:** 201 Created

#### PUT `/api/v1/vocabulary/{vocabulary_id}`

- **Description:** Update a vocabulary item (admin only)
- **Authentication:** Required (admin role)
- **Request Body:** VocabularyItem (partial update allowed)
- **Response:** 200 OK

#### DELETE `/api/v1/vocabulary/{vocabulary_id}`

- **Description:** Delete a vocabulary item (admin only)
- **Authentication:** Required (admin role)
- **Response:** 204 No Content

### 2.4 Progress Endpoints

#### GET `/api/v1/progress`

- **Description:** Get user's progress summary
- **Authentication:** Required
- **Query Parameters:**
  - `year`: YearGroup (optional, filter by year)
- **Response:** 200 OK
  ```json
  {
    "user_id": "uuid",
    "year_progress": [
      {
        "year": "year3",
        "total_words": 50,
        "mastered_words": 15,
        "mastered_percentage": 30.0
      }
    ],
    "overall_progress": {
      "total_words": 200,
      "mastered_words": 45,
      "mastered_percentage": 22.5
    }
  }
  ```


#### GET `/api/v1/progress/mastered`

- **Description:** Get list of mastered word IDs for a year
- **Authentication:** Required
- **Query Parameters:**
  - `year`: YearGroup (required)
- **Response:** 200 OK
  ```json
  {
    "year": "year3",
    "mastered_word_ids": ["uuid1", "uuid2", ...]
  }
  ```


#### POST `/api/v1/progress/mastered`

- **Description:** Mark a word as mastered
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "vocabulary_item_id": "uuid",
    "year": "year3"
  }
  ```

- **Response:** 201 Created or 200 OK (if already exists)
  ```json
  {
    "id": "uuid",
    "user_id": "uuid",
    "vocabulary_item_id": "uuid",
    "year": "year3",
    "is_mastered": true,
    "mastered_at": "datetime"
  }
  ```


#### DELETE `/api/v1/progress/mastered/{vocabulary_item_id}`

- **Description:** Unmark a word as mastered
- **Authentication:** Required
- **Query Parameters:**
  - `year`: YearGroup (required)
- **Response:** 204 No Content

#### POST `/api/v1/progress/practice`

- **Description:** Record a practice session for a word
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "vocabulary_item_id": "uuid",
    "year": "year3",
    "correct": true
  }
  ```

- **Response:** 200 OK

### 2.5 Quiz Endpoints

#### POST `/api/v1/quiz/generate`

- **Description:** Generate quiz questions from mastered words
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "year": "year3",
    "question_count": 10 (optional, default: all mastered words)
  }
  ```

- **Response:** 200 OK
  ```json
  {
    "quiz_id": "uuid",
    "year": "year3",
    "questions": [
      {
        "id": "uuid",
        "prompt": "string",
        "options": ["string"],
        "correct_index": 0,
        "type": "meaning"
      }
    ],
    "total_questions": 10
  }
  ```


#### POST `/api/v1/quiz/submit`

- **Description:** Submit quiz answers and get results
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "quiz_id": "uuid",
    "answers": [
      {
        "question_id": "uuid",
        "selected_index": 0
      }
    ]
  }
  ```

- **Response:** 200 OK
  ```json
  {
    "quiz_id": "uuid",
    "total_questions": 10,
    "correct_answers": 8,
    "incorrect_answers": 2,
    "score_percentage": 80.0,
    "results": [
      {
        "question_id": "uuid",
        "correct": true,
        "selected_index": 0,
        "correct_index": 0
      }
    ]
  }
  ```


### 2.6 Sentence Fill Endpoints

#### POST `/api/v1/sentences/generate`

- **Description:** Generate sentence fill-in-the-blank questions
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "year": "year3",
    "question_count": 10 (optional, default: all available)
  }
  ```

- **Response:** 200 OK
  ```json
  {
    "session_id": "uuid",
    "year": "year3",
    "questions": [
      {
        "id": "uuid",
        "sentence_template": "string",
        "display_sentence": "string",
        "correct_word": "string",
        "options": ["string"]
      }
    ],
    "total_questions": 10
  }
  ```


#### POST `/api/v1/sentences/submit`

- **Description:** Submit sentence fill answers
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "session_id": "uuid",
    "answers": [
      {
        "question_id": "uuid",
        "selected_word": "string"
      }
    ]
  }
  ```

- **Response:** 200 OK (similar structure to quiz submit)

### 2.7 Flashcard Endpoints

#### GET `/api/v1/flashcards`

- **Description:** Get flashcards for a year (paginated)
- **Authentication:** Required
- **Query Parameters:**
  - `year`: YearGroup (required)
  - `skip`: Integer (default: 0)
  - `limit`: Integer (default: 5, batch size)
- **Response:** 200 OK
  ```json
  {
    "cards": [
      {
        "id": "uuid",
        "year": "year3",
        "word": "string",
        "meaning": "string",
        "antonyms": ["string"],
        "example_sentences": ["string"]
      }
    ],
    "total": 50,
    "skip": 0,
    "limit": 5,
    "has_more": true
  }
  ```


## 3. Architecture & Design Patterns

### 3.1 Project Structure

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
│   │   ├── quiz_service.py     # Quiz generation logic
│   │   └── sentence_service.py # Sentence question generation
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
│   ├── unit/
│   │   ├── test_services/
│   │   ├── test_repositories/
│   │   └── test_utils/
│   ├── integration/
│   │   ├── test_api/
│   │   └── test_database/
│   └── e2e/
│       └── test_api_flows.py
│
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
│
├── requirements.txt
├── .env.example
└── README.md
```

### 3.2 Design Patterns

#### Repository Pattern

- Abstract data access layer
- Easy to swap implementations (SQLAlchemy, MongoDB, etc.)
- Testable with mock repositories

#### Service Layer Pattern

- Business logic separated from API routes
- Reusable across different interfaces (REST, GraphQL, etc.)
- Single Responsibility Principle

#### Dependency Injection

- FastAPI's dependency system for database sessions, auth, etc.
- Enables easy testing with test doubles

#### Factory Pattern

- For generating quiz questions and sentence questions
- Configurable question generation strategies

### 3.3 Technology Stack

- **Framework:** FastAPI 0.104+
- **Database:** PostgreSQL 14+ (or SQLite for development)
- **ORM:** SQLAlchemy 2.0+
- **Migrations:** Alembic
- **Authentication:** JWT (python-jose, passlib)
- **Validation:** Pydantic v2
- **Testing:** pytest, pytest-asyncio, httpx
- **Code Quality:** black, flake8, mypy, isort

## 4. Database Schema

### 4.1 Tables

#### users

- `id` UUID PRIMARY KEY
- `username` VARCHAR(50) UNIQUE NOT NULL
- `email` VARCHAR(255) UNIQUE NOT NULL
- `password_hash` VARCHAR(255) NOT NULL
- `full_name` VARCHAR(255)
- `is_active` BOOLEAN DEFAULT TRUE
- `created_at` TIMESTAMP DEFAULT NOW()
- `updated_at` TIMESTAMP DEFAULT NOW()

#### vocabulary_items

- `id` UUID PRIMARY KEY
- `year` VARCHAR(10) NOT NULL (YearGroup enum)
- `word` VARCHAR(255) NOT NULL
- `meaning` TEXT NOT NULL
- `antonyms` JSONB (array of strings)
- `example_sentences` JSONB (array of strings)
- `created_at` TIMESTAMP DEFAULT NOW()
- `updated_at` TIMESTAMP DEFAULT NOW()
- UNIQUE(year, word)

#### user_progress

- `id` UUID PRIMARY KEY
- `user_id` UUID REFERENCES users(id) ON DELETE CASCADE
- `vocabulary_item_id` UUID REFERENCES vocabulary_items(id) ON DELETE CASCADE
- `year_group` VARCHAR(10) NOT NULL
- `is_mastered` BOOLEAN DEFAULT FALSE
- `mastered_at` TIMESTAMP
- `times_practiced` INTEGER DEFAULT 0
- `last_practiced_at` TIMESTAMP
- `created_at` TIMESTAMP DEFAULT NOW()
- `updated_at` TIMESTAMP DEFAULT NOW()
- UNIQUE(user_id, vocabulary_item_id)

#### quiz_sessions (optional, for tracking quiz history)

- `id` UUID PRIMARY KEY
- `user_id` UUID REFERENCES users(id)
- `year` VARCHAR(10) NOT NULL
- `total_questions` INTEGER
- `correct_answers` INTEGER
- `completed_at` TIMESTAMP DEFAULT NOW()

### 4.2 Indexes

- `vocabulary_items(year, word)` - for filtering by year
- `user_progress(user_id, year_group, is_mastered)` - for progress queries
- `users(username)` - for login lookups
- `users(email)` - for email lookups

## 5. Security Requirements

### 5.1 Authentication

- JWT tokens with configurable expiration (default: 1 hour)
- Refresh tokens with longer expiration (default: 7 days)
- Password hashing using bcrypt (minimum 12 rounds)
- Token blacklisting for logout (optional, can use short expiration)

### 5.2 Authorization

- Role-based access control (User, Admin)
- Users can only access their own progress data
- Admin-only endpoints for vocabulary CRUD operations
- Middleware to validate JWT on protected routes

### 5.3 Data Validation

- Input validation using Pydantic schemas
- SQL injection prevention (SQLAlchemy parameterized queries)
- XSS prevention (proper content-type headers)
- Rate limiting on authentication endpoints

### 5.4 CORS

- Configurable CORS settings
- Allow specific origins (iOS app domains)
- Credentials support for authenticated requests

## 6. Testing Requirements

### 6.1 Unit Tests

- **Coverage Target:** Minimum 80%
- **Test Files:**
  - All service classes
  - Repository classes
  - Utility functions (quiz generation, etc.)
  - Security functions (password hashing, JWT)
- **Mocking:** Use pytest-mock for external dependencies

### 6.2 Integration Tests

- **API Endpoint Tests:**
  - All CRUD operations
  - Authentication flows
  - Authorization checks
  - Error handling (404, 401, 403, 422, etc.)
- **Database Tests:**
  - Repository operations with test database
  - Transaction rollback after each test
  - Foreign key constraints
- **Use TestClient:** FastAPI's TestClient for API testing

### 6.3 End-to-End Tests

- **Complete User Flows:**
  - User registration → login → vocabulary fetch → progress update → quiz generation → quiz submission
  - Multiple users with isolated progress data
- **Performance Tests:**
  - Response time < 200ms for simple queries
  - Response time < 500ms for complex queries (quiz generation)

### 6.4 Test Data

- Fixtures for common test data (users, vocabulary items)
- Factory pattern for generating test data
- Seed data for development environment

## 7. Error Handling

### 7.1 HTTP Status Codes

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST (resource created)
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server errors

### 7.2 Error Response Format

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "field": "field_name (if validation error)"
}
```

### 7.3 Custom Exceptions

- `VocabularyNotFoundError`
- `UserNotFoundError`
- `UnauthorizedError`
- `ForbiddenError`
- `ValidationError`

## 8. API Documentation

### 8.1 OpenAPI/Swagger

- Auto-generated from FastAPI
- Available at `/docs` endpoint
- Include request/response examples
- Authentication scheme documentation

### 8.2 ReDoc

- Alternative documentation at `/redoc`
- User-friendly API reference

## 9. Performance Requirements

### 9.1 Response Times

- Simple queries (GET single resource): < 100ms
- List queries with pagination: < 200ms
- Quiz generation: < 500ms
- Authentication: < 200ms

### 9.2 Scalability

- Support concurrent requests (async/await)
- Database connection pooling
- Query optimization (indexes, eager loading where needed)

### 9.3 Caching (Optional)

- Cache year groups (rarely changes)
- Cache vocabulary lists per year (with invalidation on updates)

## 10. Deployment Considerations

### 10.1 Environment Variables

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration
- `REFRESH_TOKEN_EXPIRE_DAYS` - Refresh token expiration
- `CORS_ORIGINS` - Allowed CORS origins
- `ENVIRONMENT` - dev/staging/production

### 10.2 Docker Support

- Dockerfile for containerization
- docker-compose.yml for local development (PostgreSQL + API)

### 10.3 Health Checks

- `GET /health` - Basic health check
- `GET /health/db` - Database connectivity check

## 11. Data Migration

### 11.1 Initial Data

- Seed vocabulary items from JSON files (Year3.json, Year4.json, etc.)
- Migration script to import initial vocabulary data
- Support for adding new year groups in the future

## 12. Logging

### 12.1 Log Levels

- INFO: Normal operations
- WARNING: Deprecated usage, recoverable errors
- ERROR: Exceptions, failed operations
- DEBUG: Detailed debugging (development only)

### 12.2 Log Format

- Structured logging (JSON format for production)
- Include: timestamp, level, message, user_id (if authenticated), request_id

## 13. Future Enhancements (Out of Scope but Documented)

- Analytics endpoints (learning progress over time)
- Admin dashboard API
- Bulk vocabulary import/export
- Audio pronunciation API (text-to-speech)
- Spaced repetition algorithm integration
- Multi-language support
- Social features (leaderboards, sharing progress)

---

## Implementation Notes

1. **Quiz Generation Algorithm:**

   - Select mastered words for the year
   - For each word, create a question with the word as prompt
   - Generate 3 distractors from other mastered words' meanings
   - Randomly place correct answer among options

2. **Sentence Question Generation:**

   - Filter vocabulary items with example sentences
   - Replace the word in sentence with {word} placeholder
   - Generate 3 distractors from other words
   - Randomly place correct word among options

3. **Progress Tracking:**

   - Track both mastery status and practice frequency
   - Support for future analytics (learning curve, retention rate)

4. **Database Choice:**

   - PostgreSQL recommended for production (JSONB support for arrays)
   - SQLite acceptable for development/testing
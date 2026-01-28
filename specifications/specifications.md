# Vocabulary Wizard API - Specifications Document

## Overview

This document specifies the requirements for building a FastAPI backend to support the Vocabulary Wizard iOS application. The backend provides RESTful APIs for vocabulary management, quiz generation, progress tracking, and user authentication for school children preparing for eleven plus and SAT exams in England (Levels 1-4, previously Years 3-6).

## 1. Core Data Models

### 1.1 VocabularyItem

- **Fields:**
  - `id`: UUID (primary key)
  - `word`: String (required, globally unique)
  - `meaning`: String (required)
  - `synonyms`: List[String] (words with similar meanings)
  - `antonyms`: List[String] (words with opposite meanings)
  - `example_sentences`: List[String] (sentences demonstrating word usage)
  - `created_at`: DateTime
  - `updated_at`: DateTime

- **Key Changes:**
  - Words are now globally unique (no duplicates across levels)
  - Level associations are managed through the `VocabularyLevel` relationship table
  - Removed `year` field (replaced with level associations)

### 1.2 Level

- **Fields:**
  - `id`: UUID (primary key)
  - `level`: Integer (1, 2, 3, 4) - unique
  - `name`: String (e.g., "Level 1")
  - `description`: String (optional, e.g., "Beginner (Age 7-8)")
  - `created_at`: DateTime

- **Level Mapping:**
  - Level 1: Ages 7-8 (Beginner) - Previously Year 3
  - Level 2: Ages 8-9 (Elementary) - Previously Year 4
  - Level 3: Ages 9-10 (Intermediate) - Previously Year 5
  - Level 4: Ages 10-11 (Advanced) - Previously Year 6

### 1.3 VocabularyLevel

- **Fields:**
  - `id`: UUID (primary key)
  - `vocabulary_item_id`: UUID (foreign key to VocabularyItem)
  - `level_id`: UUID (foreign key to Level)
  - `created_at`: DateTime

- **Purpose:** Association table linking vocabulary items to levels. Allows:
  - A word to be associated with multiple levels (if appropriate)
  - Querying vocabulary by level
  - Maintaining unique words in the vocabulary table

- **Unique Constraint:** (vocabulary_item_id, level_id)

### 1.4 QuizQuestion

- **Fields:**
  - `id`: UUID
  - `vocabulary_item_id`: UUID (foreign key)
  - `prompt`: String (the word to define)
  - `options`: List[String] (multiple choice options)
  - `correct_index`: Integer (0-based index of correct answer)
  - `type`: Enum (currently only "meaning")
  - `created_at`: DateTime

### 1.5 QuizSentence

- **Fields:**
  - `id`: UUID (primary key)
  - `vocabulary_item_id`: UUID (foreign key to VocabularyItem)
  - `sentence`: String (sentence with _____ blank placeholder)
  - `created_at`: DateTime

- **Purpose:** Pre-generated fill-in-the-blank sentences for sentence quizzes. Each vocabulary word has multiple associated quiz sentences.

- **Example:**
  - Word: "peaceful"
  - Sentence: "The countryside is beautiful and _____."

### 1.6 SentenceQuestion (Runtime Model)

- **Fields:**
  - `id`: UUID
  - `sentence_template`: String (sentence with {word} placeholder)
  - `display_sentence`: String (sentence with _____ for display)
  - `correct_word`: String
  - `options`: List[String] (multiple choice options)
  - `vocabulary_item_id`: UUID (foreign key)
  - `created_at`: DateTime

### 1.7 User

- **Fields:**
  - `id`: UUID (primary key)
  - `username`: String (unique, required)
  - `email`: String (unique, required, validated)
  - `password_hash`: String (hashed, never exposed)
  - `full_name`: String (optional)
  - `created_at`: DateTime
  - `updated_at`: DateTime
  - `is_active`: Boolean (default: True)

### 1.8 UserProgress

- **Fields:**
  - `id`: UUID (primary key)
  - `user_id`: UUID (foreign key)
  - `vocabulary_item_id`: UUID (foreign key)
  - `year_group`: String (deprecated, kept for backward compatibility)
  - `is_mastered`: Boolean (default: False)
  - `mastered_at`: DateTime (nullable)
  - `times_practiced`: Integer (default: 0)
  - `last_practiced_at`: DateTime (nullable)
  - `created_at`: DateTime
  - `updated_at`: DateTime
  - **Unique constraint:** (user_id, vocabulary_item_id)

- **Note:** The `year_group` field is kept for backward compatibility but should be replaced with level-based queries in future versions.

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

### 2.2 Level Endpoints

#### GET `/api/v1/levels`

- **Description:** Get all available levels
- **Authentication:** Optional (public endpoint)
- **Response:** 200 OK
  ```json
  [
    {
      "id": "uuid",
      "level": 1,
      "name": "Level 1",
      "description": "Beginner (Age 7-8)",
      "created_at": "datetime"
    }
  ]
  ```

### 2.3 Vocabulary Item Endpoints

#### GET `/api/v1/vocabulary`

- **Description:** Get vocabulary items with optional filters
- **Authentication:** Required
- **Query Parameters:**
  - `level`: Integer (optional, filter by level: 1, 2, 3, or 4)
  - `skip`: Integer (default: 0, pagination)
  - `limit`: Integer (default: 100, pagination)
  - `search`: String (optional, search word/meaning)
- **Response:** 200 OK
  ```json
  {
    "items": [
      {
        "id": "uuid",
        "word": "string",
        "meaning": "string",
        "synonyms": ["string"],
        "antonyms": ["string"],
        "example_sentences": ["string"],
        "levels": [1, 2],
        "created_at": "datetime",
        "updated_at": "datetime"
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
- **Response:** 200 OK (single VocabularyItem object with levels array)

#### POST `/api/v1/vocabulary`

- **Description:** Create a new vocabulary item (admin only)
- **Authentication:** Required (admin role)
- **Request Body:**
  ```json
  {
    "word": "string",
    "meaning": "string",
    "synonyms": ["string"],
    "antonyms": ["string"],
    "example_sentences": ["string"],
    "levels": [1, 2]
  }
  ```
- **Response:** 201 Created

#### PUT `/api/v1/vocabulary/{vocabulary_id}`

- **Description:** Update a vocabulary item (admin only)
- **Authentication:** Required (admin role)
- **Request Body:** VocabularyItem (partial update allowed, including levels)
- **Response:** 200 OK

#### DELETE `/api/v1/vocabulary/{vocabulary_id}`

- **Description:** Delete a vocabulary item (admin only)
- **Authentication:** Required (admin role)
- **Response:** 204 No Content

### 2.4 Quiz Sentence Endpoints

#### GET `/api/v1/vocabulary/{vocabulary_id}/quiz-sentences`

- **Description:** Get all quiz sentences for a specific vocabulary item
- **Authentication:** Required
- **Response:** 200 OK
  ```json
  {
    "vocabulary_item_id": "uuid",
    "word": "peaceful",
    "sentences": [
      {
        "id": "uuid",
        "sentence": "The countryside is beautiful and _____.",
        "created_at": "datetime"
      }
    ],
    "total": 10
  }
  ```


#### GET `/api/v1/quiz-sentences`

- **Description:** Get quiz sentences with optional filters
- **Authentication:** Required
- **Query Parameters:**
  - `level`: Integer (optional, filter by level: 1, 2, 3, or 4)
  - `skip`: Integer (default: 0, pagination)
  - `limit`: Integer (default: 100, pagination)
- **Response:** 200 OK
  ```json
  {
    "items": [
      {
        "id": "uuid",
        "vocabulary_item_id": "uuid",
        "word": "string",
        "sentence": "string",
        "created_at": "datetime"
      }
    ],
    "total": 2000,
    "skip": 0,
    "limit": 100
  }
  ```


### 2.5 Progress Endpoints

#### GET `/api/v1/progress`

- **Description:** Get user's progress summary
- **Authentication:** Required
- **Query Parameters:**
  - `level`: Integer (optional, filter by level: 1, 2, 3, or 4)
- **Response:** 200 OK
  ```json
  {
    "user_id": "uuid",
    "level_progress": [
      {
        "level": 1,
        "total_words": 246,
        "mastered_words": 50,
        "mastered_percentage": 20.3
      }
    ],
    "overall_progress": {
      "total_words": 801,
      "mastered_words": 150,
      "mastered_percentage": 18.7
    }
  }
  ```


#### GET `/api/v1/progress/mastered`

- **Description:** Get list of mastered word IDs for a level
- **Authentication:** Required
- **Query Parameters:**
  - `level`: Integer (required: 1, 2, 3, or 4)
- **Response:** 200 OK
  ```json
  {
    "level": 1,
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
    "level": 1
  }
  ```

- **Response:** 201 Created or 200 OK (if already exists)
  ```json
  {
    "id": "uuid",
    "user_id": "uuid",
    "vocabulary_item_id": "uuid",
    "year_group": "year3",
    "is_mastered": true,
    "mastered_at": "datetime"
  }
  ```


#### DELETE `/api/v1/progress/mastered/{vocabulary_item_id}`

- **Description:** Unmark a word as mastered
- **Authentication:** Required
- **Query Parameters:**
  - `level`: Integer (required: 1, 2, 3, or 4)
- **Response:** 204 No Content

#### POST `/api/v1/progress/practice`

- **Description:** Record a practice session for a word
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "vocabulary_item_id": "uuid",
    "level": 1,
    "correct": true
  }
  ```

- **Response:** 200 OK

### 2.6 Quiz Endpoints

#### POST `/api/v1/quiz/generate`

- **Description:** Generate quiz questions from mastered words
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "level": 1,
    "question_count": 10
  }
  ```

- **Response:** 200 OK
  ```json
  {
    "quiz_id": "uuid",
    "level": 1,
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


### 2.7 Sentence Fill Endpoints

#### POST `/api/v1/sentences/generate`

- **Description:** Generate sentence fill-in-the-blank questions from pre-stored quiz sentences
- **Authentication:** Required
- **Request Body:**
  ```json
  {
    "level": 1,
    "question_count": 10
  }
  ```

- **Response:** 200 OK
  ```json
  {
    "session_id": "uuid",
    "level": 1,
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

### 2.8 Flashcard Endpoints

#### GET `/api/v1/flashcards`

- **Description:** Get flashcards for a level (paginated)
- **Authentication:** Required
- **Query Parameters:**
  - `level`: Integer (required: 1, 2, 3, or 4)
  - `skip`: Integer (default: 0)
  - `limit`: Integer (default: 5, batch size)
- **Response:** 200 OK
  ```json
  {
    "cards": [
      {
        "id": "uuid",
        "word": "string",
        "meaning": "string",
        "synonyms": ["string"],
        "antonyms": ["string"],
        "example_sentences": ["string"],
        "levels": [1]
      }
    ],
    "total": 246,
    "skip": 0,
    "limit": 5,
    "has_more": true
  }
  ```


## 3. Architecture & Design Patterns

### 3.1 Project Structure

```
vocabularyWizardAPI/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
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
│   │       ├── flashcards.py   # Flashcard routes
│   │       └── levels.py       # Level routes
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # JWT, password hashing
│   │   ├── config.py           # Settings (Pydantic)
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── token_blacklist.py  # Token management
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User SQLAlchemy model
│   │   ├── vocabulary.py       # VocabularyItem model
│   │   ├── level.py             # Level and VocabularyLevel models
│   │   ├── quiz_sentence.py    # QuizSentence model
│   │   ├── progress.py         # UserProgress model
│   │   ├── quiz.py             # QuizQuestion model
│   │   └── common.py           # Common model utilities
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   │   ├── vocabulary.py       # VocabularyItem schemas
│   │   ├── level.py             # Level schemas
│   │   ├── quiz_sentence.py    # QuizSentence schemas
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
│   │   ├── level_repository.py  # Level and VocabularyLevel repositories
│   │   ├── quiz_sentence_repository.py
│   │   └── progress_repository.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── quiz_generator.py   # Quiz and sentence generation (local templates)
│
├── data/
│   ├── vocabulary.csv           # Unified vocabulary (unique words)
│   ├── vocabulary_levels.csv   # Word-level associations
│   ├── quiz_sentences_level1.csv
│   ├── quiz_sentences_level2.csv
│   ├── quiz_sentences_level3.csv
│   └── quiz_sentences_level4.csv
│
├── scripts/
│   ├── import_vocabulary_levels.py
│   └── import_quiz_sentences_levels.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api_integration.py
│   ├── test_auth.py
│   └── test_vocabulary.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
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
- `word` VARCHAR(255) UNIQUE NOT NULL (globally unique)
- `meaning` TEXT NOT NULL
- `synonyms` JSONB (array of strings)
- `antonyms` JSONB (array of strings)
- `example_sentences` JSONB (array of strings)
- `created_at` TIMESTAMP DEFAULT NOW()
- `updated_at` TIMESTAMP DEFAULT NOW()

#### levels

- `id` UUID PRIMARY KEY
- `level` INTEGER UNIQUE NOT NULL (1, 2, 3, 4)
- `name` VARCHAR(50) NOT NULL
- `description` VARCHAR(255)
- `created_at` TIMESTAMP DEFAULT NOW()

#### vocabulary_levels

- `id` UUID PRIMARY KEY
- `vocabulary_item_id` UUID REFERENCES vocabulary_items(id) ON DELETE CASCADE
- `level_id` UUID REFERENCES levels(id) ON DELETE CASCADE
- `created_at` TIMESTAMP DEFAULT NOW()
- UNIQUE(vocabulary_item_id, level_id)

#### quiz_sentences

- `id` UUID PRIMARY KEY
- `vocabulary_item_id` UUID REFERENCES vocabulary_items(id) ON DELETE CASCADE
- `sentence` TEXT NOT NULL
- `created_at` TIMESTAMP DEFAULT NOW()
- INDEX(vocabulary_item_id)

#### user_progress

- `id` UUID PRIMARY KEY
- `user_id` UUID REFERENCES users(id) ON DELETE CASCADE
- `vocabulary_item_id` UUID REFERENCES vocabulary_items(id) ON DELETE CASCADE
- `year_group` VARCHAR(10) NOT NULL (deprecated, kept for backward compatibility)
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
- `level` INTEGER NOT NULL
- `total_questions` INTEGER
- `correct_answers` INTEGER
- `completed_at` TIMESTAMP DEFAULT NOW()

### 4.2 Indexes

- `vocabulary_items(word)` - for word lookups (unique index)
- `levels(level)` - for level lookups (unique index)
- `vocabulary_levels(vocabulary_item_id, level_id)` - for level filtering
- `quiz_sentences(vocabulary_item_id)` - for fetching sentences by word
- `user_progress(user_id, vocabulary_item_id)` - for progress queries
- `users(username)` - for login lookups
- `users(email)` - for email lookups

### 4.3 Entity Relationship Diagram

```
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ password_hash   │
│ full_name       │
│ is_active       │
│ created_at      │
│ updated_at      │
└────────┬────────┘
         │
         │
         ▼
┌─────────────────────┐
│   user_progress     │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ vocabulary_item_id  │
│ year_group          │
│ is_mastered         │
│ mastered_at         │
│ times_practiced     │
│ last_practiced_at   │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │
           ▼
┌─────────────────────┐       ┌─────────────────────┐
│  vocabulary_items  │       │      levels         │
├─────────────────────┤       ├─────────────────────┤
│ id (PK)             │       │ id (PK)             │
│ word (UNIQUE)       │       │ level (UNIQUE)      │
│ meaning             │       │ name                │
│ synonyms (JSONB)    │       │ description         │
│ antonyms (JSONB)    │       │ created_at          │
│ example_sentences   │       └──────────┬──────────┘
│ created_at          │                  │
│ updated_at          │                  │
└──────────┬──────────┘                  │
           │                              │
           │    ┌─────────────────────────┘
           │    │
           │    ▼
           │  ┌─────────────────────┐
           │  │ vocabulary_levels   │
           │  ├─────────────────────┤
           │  │ id (PK)             │
           │  │ vocabulary_item_id  │
           │  │ level_id            │
           │  │ created_at          │
           │  └─────────────────────┘
           │
           │
           ▼
┌─────────────────────┐
│   quiz_sentences    │
├─────────────────────┤
│ id (PK)             │
│ vocabulary_item_id  │
│ sentence            │
│ created_at          │
└─────────────────────┘
```

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

## 6. Data Requirements

### 6.1 Vocabulary Data

The vocabulary system uses globally unique words organized by levels:

- **Total unique words:** 801
- **Words can appear in multiple levels** if appropriate (149 words appear in multiple levels)

| Level | Word Count | Age Range | Difficulty | Previously |
|-------|------------|-----------|------------|------------|
| Level 1 | 246 | 7-8 | Beginner | Year 3 |
| Level 2 | 248 | 8-9 | Elementary | Year 4 |
| Level 3 | 244 | 9-10 | Intermediate | Year 5 |
| Level 4 | 234 | 10-11 | Advanced | Year 6 |

Each vocabulary word includes:
- Word (globally unique)
- Meaning (child-friendly definition)
- Synonyms (2-3 similar words)
- Antonyms (2-3 opposite words)
- Example sentences (1-2 usage examples)
- Level associations (one or more levels: 1, 2, 3, or 4)

### 6.2 Quiz Sentences

Each vocabulary word has multiple associated fill-in-the-blank quiz sentences.

- Format: Sentence with `_____` blank placeholder
- Purpose: Test word usage in context
- Total: ~6,000+ quiz sentences across all levels

| Level | Sentences |
|-------|-----------|
| Level 1 | ~2,249 sentences |
| Level 2 | ~1,325 sentences |
| Level 3 | ~1,853 sentences |
| Level 4 | ~1,602 sentences |

### 6.3 CSV Data Format

#### Vocabulary CSV Format

**vocabulary.csv:**
```csv
word,meaning,synonyms,antonyms,example_sentences
abundant,having a lot of something; plentiful,plentiful;lots;plenty,scarce;rare;few,The garden was abundant with colorful flowers.
```

**vocabulary_levels.csv:**
```csv
word,level
abundant,1
abundant,2
```

- Lists use semicolon (`;`) as separator within fields
- Words are globally unique in vocabulary.csv
- Level associations are in vocabulary_levels.csv

#### Quiz Sentences CSV Format

```csv
level,word,sentence
1,abundant,The forest was _____ with wildlife.
1,abundant,There was an _____ supply of fresh water.
```

## 7. Testing Requirements

### 7.1 Unit Tests

- **Coverage Target:** Minimum 80%
- **Test Files:**
  - All service classes
  - Repository classes
  - Utility functions (quiz generation, etc.)
  - Security functions (password hashing, JWT)
- **Mocking:** Use pytest-mock for external dependencies

### 7.2 Integration Tests

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

### 7.3 End-to-End Tests

- **Complete User Flows:**
  - User registration → login → vocabulary fetch → progress update → quiz generation → quiz submission
  - Multiple users with isolated progress data
- **Performance Tests:**
  - Response time < 200ms for simple queries
  - Response time < 500ms for complex queries (quiz generation)

## 8. Error Handling

### 8.1 HTTP Status Codes

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST (resource created)
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server errors

### 8.2 Error Response Format

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "field": "field_name (if validation error)"
}
```

### 8.3 Custom Exceptions

- `VocabularyNotFoundError`
- `QuizSentenceNotFoundError`
- `LevelNotFoundError`
- `UserNotFoundError`
- `UnauthorizedError`
- `ForbiddenError`
- `ValidationError`

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

- Cache levels (rarely changes)
- Cache vocabulary lists per level (with invalidation on updates)

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

## 11. Implementation Notes

1. **Level-Based System:**
   - Words are globally unique (no duplicates)
   - Level associations allow words to appear in multiple levels
   - Migration script converts old year-based data to new format

2. **Quiz Generation Algorithm:**
   - Select mastered words for the level
   - For each word, create a question with the word as prompt
   - Generate 3 distractors from other mastered words' meanings
   - Randomly place correct answer among options

3. **Sentence Question Generation:**
   - Fetch pre-stored quiz sentences from database
   - Filter by level through vocabulary-level associations
   - Generate 3 distractors from other words in the same level
   - Randomly place correct word among options

4. **Progress Tracking:**
   - Track both mastery status and practice frequency
   - Support for future analytics (learning curve, retention rate)
   - Level-based progress queries

5. **Database Choice:**
   - PostgreSQL recommended for production (JSONB support for arrays)
   - SQLite acceptable for development/testing

6. **Data Import:**
   - Use `scripts/import_vocabulary_levels.py` to import vocabulary and level associations
   - Use `scripts/import_quiz_sentences_levels.py` to import quiz sentences by level
   - Data files: vocabulary.csv, vocabulary_levels.csv, quiz_sentences_level*.csv

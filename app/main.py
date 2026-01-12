from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import Base, engine
from app.api.v1 import auth, vocabulary, progress, quiz, sentences, flashcards, years

# Import models to ensure they're registered with SQLAlchemy
from app.models import user, vocabulary as vocab_model, progress as progress_model, quiz as quiz_model

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vocabulary Wizard API",
    description="FastAPI backend for Vocabulary iOS application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(years.router, prefix=f"{settings.API_V1_PREFIX}/years", tags=["Year Groups"])
app.include_router(vocabulary.router, prefix=f"{settings.API_V1_PREFIX}/vocabulary", tags=["Vocabulary"])
app.include_router(progress.router, prefix=f"{settings.API_V1_PREFIX}/progress", tags=["Progress"])
app.include_router(quiz.router, prefix=f"{settings.API_V1_PREFIX}/quiz", tags=["Quiz"])
app.include_router(sentences.router, prefix=f"{settings.API_V1_PREFIX}/sentences", tags=["Sentences"])
app.include_router(flashcards.router, prefix=f"{settings.API_V1_PREFIX}/flashcards", tags=["Flashcards"])


@app.get("/health")
def health_check():
    """Basic health check."""
    return {"status": "healthy"}


@app.get("/health/db")
def health_check_db():
    """Database connectivity check."""
    try:
        from app.database import SessionLocal
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Vocabulary Wizard API",
        "version": "1.0.0",
        "docs": "/docs"
    }


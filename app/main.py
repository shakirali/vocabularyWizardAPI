import logging
import warnings

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.api.v1 import (auth, flashcards, progress, quiz, sentences,
                        vocabulary)
from app.core.config import settings
from app.database import Base, engine
# Import models to ensure they're registered with SQLAlchemy
from app.models import progress as progress_model  # noqa: F401
from app.models import quiz as quiz_model  # noqa: F401
from app.models import user  # noqa: F401
from app.models import vocabulary as vocab_model  # noqa: F401

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Suppress deprecation warning from python-jose library (third-party issue)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="jose")

# Create database tables
Base.metadata.create_all(bind=engine)

# Rate limiter configuration
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title="Vocabulary Wizard API",
    description="FastAPI backend for Vocabulary iOS application",
    version="1.0.0",
)

# Add rate limiter to app state
app.state.limiter = limiter

# Add rate limiting middleware
app.add_middleware(SlowAPIMiddleware)

# Custom rate limit exceeded handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(f"Rate limit exceeded for {get_remote_address(request)}")
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."},
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
app.include_router(
    auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"]
)
app.include_router(
    vocabulary.router,
    prefix=f"{settings.API_V1_PREFIX}/vocabulary",
    tags=["Vocabulary"],
)
app.include_router(
    progress.router, prefix=f"{settings.API_V1_PREFIX}/progress", tags=["Progress"]
)
app.include_router(quiz.router, prefix=f"{settings.API_V1_PREFIX}/quiz", tags=["Quiz"])
app.include_router(
    sentences.router, prefix=f"{settings.API_V1_PREFIX}/sentences", tags=["Sentences"]
)
app.include_router(
    flashcards.router,
    prefix=f"{settings.API_V1_PREFIX}/flashcards",
    tags=["Flashcards"],
)


@app.get("/health")
def health_check():
    """Basic health check."""
    return {"status": "healthy"}


@app.get("/health/db")
def health_check_db():
    """Database connectivity check."""
    try:
        from sqlalchemy import text

        from app.database import SessionLocal

        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Vocabulary Wizard API", "version": "1.0.0", "docs": "/docs"}

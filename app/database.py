from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def clean_database(create_default_levels: bool = True):
    """
    Drop all tables and recreate them.
    
    WARNING: This will delete ALL data in the database!
    
    Args:
        create_default_levels: If True, create default level records (1-4) after recreating tables
    
    Returns:
        None
    """
    from app.repositories.level_repository import LevelRepository
    
    # Import all models to ensure they're registered with Base.metadata
    from app.models import level, progress, quiz, quiz_sentence, user, vocabulary  # noqa: F401
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create default levels if requested
    if create_default_levels:
        db = SessionLocal()
        try:
            level_repo = LevelRepository(db)
            level_repo.create_default_levels()
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

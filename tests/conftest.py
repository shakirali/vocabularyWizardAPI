import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app, limiter
from app.api.v1.auth import limiter as auth_limiter
import uuid

# Test database (SQLite in memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Ensure levels exist
    from app.repositories.level_repository import LevelRepository
    level_repo = LevelRepository(db)
    level_repo.create_default_levels()
    
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override and disabled rate limiting."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Disable rate limiting for tests
    limiter.enabled = False
    auth_limiter.enabled = False
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Re-enable rate limiting after tests
    limiter.enabled = True
    auth_limiter.enabled = True
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data():
    """Test user data with strong password."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123",  # Meets requirements: uppercase, lowercase, digit
        "full_name": "Test User"
    }


@pytest.fixture
def test_admin_user(db_session):
    """Create an admin user directly in the database for testing admin-only endpoints."""
    from app.models.user import User
    from app.core.security import get_password_hash
    
    admin = User(
        id=uuid.uuid4(),
        username="adminuser",
        email="admin@example.com",
        password_hash=get_password_hash("AdminPassword123"),
        full_name="Admin User",
        is_admin=True,
        is_active=True,
        token_version=0,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return {
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "AdminPassword123",
        "user": admin,
    }


@pytest.fixture
def test_vocabulary_data():
    """Test vocabulary item data with levels."""
    return {
        "word": "example",
        "meaning": "a thing characteristic of its kind",
        "synonyms": ["instance", "sample"],
        "antonyms": ["counterexample"],
        "example_sentences": ["This is an example sentence."],
        "levels": [1]  # Level 1 (previously year3)
    }

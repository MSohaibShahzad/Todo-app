"""Test configuration and fixtures."""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from src.auth.jwt import create_access_token
from src.database import get_session
from src.main import app
from src.models.task import Task
from src.models.user import User

# Test database URL (use in-memory SQLite for fast tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def engine():
    """Create test database engine."""
    test_engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True,
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield test_engine

    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session_maker = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client."""
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_a(db_session: AsyncSession) -> User:
    """Create test user A."""
    # Use a pre-hashed password to avoid bcrypt issues in tests
    # This is "password123" hashed with bcrypt
    user = User(
        email="user_a@example.com",
        name="User A",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqKvZ.KCqC",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def user_b(db_session: AsyncSession) -> User:
    """Create test user B."""
    # Use a pre-hashed password to avoid bcrypt issues in tests
    # This is "password123" hashed with bcrypt
    user = User(
        email="user_b@example.com",
        name="User B",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqKvZ.KCqC",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers_user_a(user_a: User) -> dict:
    """Get auth headers for user A."""
    token = create_access_token({"user_id": user_a.id})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_user_b(user_b: User) -> dict:
    """Get auth headers for user B."""
    token = create_access_token({"user_id": user_b.id})
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def task_user_a(db_session: AsyncSession, user_a: User) -> Task:
    """Create task for user A."""
    task = Task(
        user_id=user_a.id,
        title="User A's Task",
        description="This belongs to User A",
        completed=False,
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


@pytest_asyncio.fixture
async def task_user_b(db_session: AsyncSession, user_b: User) -> Task:
    """Create task for user B."""
    task = Task(
        user_id=user_b.id,
        title="User B's Task",
        description="This belongs to User B",
        completed=False,
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task

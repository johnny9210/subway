"""Pytest Configuration"""
import pytest
from httpx import AsyncClient

from app.main import app


@pytest.fixture
async def client():
    """비동기 테스트 클라이언트"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

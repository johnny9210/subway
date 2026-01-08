"""Redis Cache Configuration"""
from typing import Optional
import json

import redis.asyncio as redis

from app.config import settings


class RedisCache:
    """Redis 캐시 클라이언트"""

    def __init__(self):
        self.redis: Optional[redis.Redis] = None

    async def connect(self):
        """Redis 연결"""
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)

    async def disconnect(self):
        """Redis 연결 해제"""
        if self.redis:
            await self.redis.close()

    async def get(self, key: str) -> Optional[dict]:
        """캐시 조회"""
        if not self.redis:
            return None
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict, ttl: int = 60):
        """캐시 저장"""
        if not self.redis:
            return
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def delete(self, key: str):
        """캐시 삭제"""
        if not self.redis:
            return
        await self.redis.delete(key)


# 싱글톤 인스턴스
cache = RedisCache()


async def get_cache() -> RedisCache:
    """캐시 의존성"""
    return cache

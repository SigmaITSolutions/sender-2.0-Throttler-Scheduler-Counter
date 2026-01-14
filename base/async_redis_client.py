import redis.asyncio as redis

class AsyncRedisClient:
    def __init__(self, url="redis://localhost:6379/0"):
        self.redis_url = url
        self.client = None

    async def connect(self):
        """Creates the connection client."""
        if self.client is None:
            self.client = redis.from_url(self.redis_url, decode_responses=True)
        return self.client

    async def get(self, key):
        return await self.client.get(key)

    async def set(self, key, value):
        await self.client.set(key, value)

    async def close(self):
        """Closes the connection."""
        if self.client:
            await self.client.close()
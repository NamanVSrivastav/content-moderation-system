import redis

class CacheService:
    def __init__(self):
        self.redis = redis.Redis(host="redis", port=6379, db=0)

    def get(self, key: str):
        return self.redis.get(key)

    def set(self, key: str, value: str, ttl: int = 3600):
        self.redis.set(key, value, ex=ttl)
import redis.asyncio
from fastapi_users.authentication import BearerTransport, RedisStrategy, AuthenticationBackend
from src.config import REDIS_HOST, REDIS_PORT, REDIS_STRATEGY_LIFETIME

bearer_transport = BearerTransport(tokenUrl="auth/login")

# Redis используется для хранения токенов в формате словарика {user.id:token}
REDIS_INSTANCE = redis.asyncio.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(REDIS_INSTANCE, lifetime_seconds=REDIS_STRATEGY_LIFETIME)


auth_backend = AuthenticationBackend(
    name="backend",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)

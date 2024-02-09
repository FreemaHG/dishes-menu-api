import redis  # type: ignore
from src.config import REDIS_HOST, REDIS_PORT

# Для добавления данных в кэш используется пакет fastapi_redis (клиент с асинхронным запросом к БД)
# Синхронный redis используется в фоновых задачах при очистке кэша,
# т.к. в BackgroundTasks нельзя передавать асинхронные функции!
redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

import redis
import threading
from django.conf import settings


class SingletonMeta(type):
    _instance_lock = threading.Lock()
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class RedisConnection(metaclass=SingletonMeta):
    def __init__(self, host='localhost', port=6379, db_number=0):
        self._redis = redis.Redis(host=host, port=port, db=db_number)

    def get_redis(self):
        return self._redis
  
    
redis_connection = RedisConnection(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db_number=settings.REDIS_DB_NUMBER
).get_redis()
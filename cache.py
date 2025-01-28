import redis
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # Usa a variável de ambiente ou o nome do serviço no Docker
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

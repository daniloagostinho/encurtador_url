import redis
import os

# Obter o host do Redis do ambiente (definido no docker-compose.yml)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

# Criar conexão com o Redis
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

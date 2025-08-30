import redis
from django.conf import settings

redis_client = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)

CODE_TTL = 300  

def set_confirmation_code(user_id: int, code: str):
    key = f"user:{user_id}:confirmation_code"
    redis_client.set(key, code, ex=CODE_TTL)

def get_confirmation_code(user_id: int):
    key = f"user:{user_id}:confirmation_code"
    return redis_client.get(key)

def delete_confirmation_code(user_id: int):
    key = f"user:{user_id}:confirmation_code"
    redis_client.delete(key)

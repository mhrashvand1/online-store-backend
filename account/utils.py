from config import settings
from random import choices
from string import digits
from common.utils import hash_string

CODE_LENGTH = getattr(settings, "CODE_LENGTH", 6)
EXPIRE_TIME = getattr(settings, "CODE_EXPIRE_TIME", 5)

def generate_random_code(length=CODE_LENGTH):
    return "".join(choices(digits, k=length))

redis_connection = settings.redis_connection

def redis_store_code(phone_number, raw_code):
    code = hash_string(raw_code)
    redis_connection.set(phone_number, code)
    redis_connection.expire(phone_number, EXPIRE_TIME*60) # Set TTL 

def redis_retrieve_code(phone_number):
    return redis_connection.get(phone_number)

from config import settings
from random import choices
from string import digits
from common.utils import hash_string
from rest_framework_simplejwt.tokens import RefreshToken


CODE_LENGTH = getattr(settings, "CODE_LENGTH", 6)
EXPIRE_TIME = getattr(settings, "CODE_EXPIRE_TIME", 5)

def generate_random_code(length=CODE_LENGTH):
    return "".join(choices(digits, k=length))

redis_connection = settings.redis_connection

def store_code(phone_number, raw_code):
    code = hash_string(raw_code)
    redis_connection.set(phone_number, code)
    redis_connection.expire(phone_number, EXPIRE_TIME*60) # Set TTL 

def retrieve_code(phone_number):
    code = redis_connection.get(phone_number)
    if code:
        return code.decode("utf-8") 

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
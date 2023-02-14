from django.core.management.base import BaseCommand
from config.settings import REDIS_HOST, REDIS_PORT, REDIS_DB_NUMBER
from redis import Redis

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        try:
            r = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_NUMBER)
            r.ping()
        except:
            raise Exception("Redis server is not loaded")
            


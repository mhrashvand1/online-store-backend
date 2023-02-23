from django.core.management.base import BaseCommand
from redis import Redis
from django.conf import settings


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        try:
            r = Redis(
                host=settings.REDIS_HOST, 
                port=settings.REDIS_PORT, 
                db=settings.REDIS_DB_NUMBER
            )
            r.ping()
        except:
            raise Exception("Redis server is not loaded")
            


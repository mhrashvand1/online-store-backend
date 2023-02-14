from account.models import User, Address, Location
from django.core.management.base import BaseCommand
from config import settings
from django.db import transaction


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--phone_number', type=str, help='phone number',
            default=settings.DEFAULT_SUPERUSER_PHONENUMBER
        )
        parser.add_argument(
            '--first_name', type=str, help='first number',
            default=settings.DEFAULT_SUPERUSER_FIRST_NAME
        )
        parser.add_argument(
            '--last_name', type=str, help='last name',
            default=settings.DEFAULT_SUPERUSER_LAST_NAME
        )
        parser.add_argument(
            '--password', type=str, help='password',
            default=settings.DEFAULT_SUPERUSER_PASSWORD
        )

    def handle(self, *args, **kwargs):        
        try:
            with transaction.atomic():
                u, created = User.objects.get_or_create(
                    phone_number=kwargs["phone_number"],
                )
                u.first_name=kwargs["first_name"],
                u.last_name=kwargs["last_name"]
                u.set_password(kwargs["password"])
                u.is_superuser = True
                u.is_staff = True
                u.save()
                Address.objects.get_or_create(user=u)
                Location.objects.get_or_create(user=u)
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
        except:
            self.stdout.write(self.style.ERROR("Error while creating superuser"))


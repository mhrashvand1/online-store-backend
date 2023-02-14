from account.models import User, Address, Location
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.crypto import get_random_string

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'phone_number', type=str, help='phone number',
        )
        parser.add_argument(
            '--first_name', type=str, help='first number',
            default=get_random_string(length=5)
        )
        parser.add_argument(
            '--last_name', type=str, help='last name',
            default=get_random_string(length=5)
        )
        parser.add_argument(
            '--password', type=str, help='password',
            default=get_random_string(length=12)
        )

    def handle(self, *args, **kwargs):        
        try:
            with transaction.atomic():
                u, created = User.objects.get_or_create(
                    phone_number=kwargs["phone_number"],
                )
                u.first_name=kwargs["first_name"]
                u.last_name=kwargs["last_name"]
                u.set_password(kwargs["password"])
                u.is_superuser = True
                u.is_staff = True
                u.save()
                Address.objects.get_or_create(user=u)
                Location.objects.get_or_create(user=u)
            if created:
                self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
            else:
                self.stdout.write(self.style.SUCCESS("A Superuser with send phone_number already exists."))        
        except:
            self.stdout.write(self.style.ERROR("Error while creating superuser"))


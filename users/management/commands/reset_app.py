from django.core.management.base import BaseCommand, CommandError

from users.models import User
from oauth2_provider.models import Application
from django.core import management


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        management.call_command("makemigrations")
        management.call_command("migrate")

        print("Running setup:")
        print("\tCreating supperuser...", end='')
        user = User.objects.create(username="admin", email="admin@example.com", is_active=True, is_superuser=True,
                                   is_staff=True)
        user.set_password("111111")
        user.save()
        print("OK")

        print("\tCreating group and Oauth application...", end='')
        user.groups.create(name="admin")
        Application.objects.create(user=user, client_type="confidential", authorization_grant_type="password")
        print("OK")

        print("\tCreate some users... ", end='')
        for x in range(5):
            tail = str(x+1)
            user = User(username="users" + tail, is_active=True, first_name="users"+tail, last_name="ln"+tail)
            user.set_password("111111")
            user.save()
        print("OK")

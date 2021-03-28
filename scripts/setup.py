import subprocess
from users.models import User
from oauth2_provider.models import Application
from django.core import management

management.call_command("reset_db", "--noinput")
management.call_command("makemigrations")
management.call_command("migrate")

user = User.objects.create(username="admin", email="admin@example.com", is_active=True)
user.set_password("111111")
user.save()

user.groups.create(name="admin")
Application.objects.create(user=user, client_type="confidential", authorization_grant_type="password")

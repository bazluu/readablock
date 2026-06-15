import secrets
import string

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from core import models
from app import services


class Command(BaseCommand):
    help = "Create a new user with a randomly generated password"

    def add_arguments(self, parser):
        parser.add_argument("email", type=str, help="Email address for the new user")
        parser.add_argument("--superuser", action="store_true", help="Create a superuser instead of a regular user")

    def handle(self, *args, **options):
        email = options["email"]
        is_superuser = options["superuser"]

        username = services.convert_email_to_username(email)

        if User.objects.filter(email=email).exists():
            raise CommandError(f'User with email "{email}" already exists')

        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = "".join(secrets.choice(alphabet) for _ in range(20))

        if is_superuser:
            user = User.objects.create_superuser(username=username, email=email, password=password)
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
        models.UserMeta.objects.create(user_id=user.id)

        self.stdout.write(email)
        self.stdout.write(password)

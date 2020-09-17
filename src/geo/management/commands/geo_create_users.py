from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = """
Creates default users

Use with
`python manage.py geo_create_users`
"""

    def handle(self, *args, **options):
        User = get_user_model()
        users = ('user1', 'user2')
        for user in users:
            try:
                User.objects.create_user(user, password=user)
            except IntegrityError:
                raise CommandError('"{0}" already exists'.format(user))

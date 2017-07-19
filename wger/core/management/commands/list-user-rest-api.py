from django.core.management.base import BaseCommand
from tabulate import tabulate

from wger.core.models import ApiUser


class Command(BaseCommand):
    help = 'List all users'

    def handle(self, *args, **options):

        all_users = [(user.user.username, user.user.email, user.created_by)
                     for user in ApiUser.objects.all()]
        print(tabulate(all_users, headers=('Username', 'Email', 'Created by')))

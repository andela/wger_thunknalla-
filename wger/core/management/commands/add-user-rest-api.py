import re

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.validators import validate_email

from wger.core.api.serializers import UserCreationSerializer
from wger.core.models import ApiUser


class Command(BaseCommand):
    help = 'Create ApiUser via Terminal'

    def add_arguments(self, parser):
        '''
        Arguments for create user via Terminal
        '''
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('created_by', type=str)

    def handle(self, *args, **options):
        '''
        Logic to handle creating user via Terminal
        '''
        data = {
            'email': options.get('email'),
            'password': options.get('password'),
            'username': options.get('username')
        }
        try:
            validate_email(data.get('email'))
        except Exception:
            self.stdout.write(self.style.ERROR("Error: Invalid email"))
            return
        if not re.match("^[A-Za-z0-9]+\s?[A-Za-z0-9]+$", data.get('username')):
            self.stdout.write(self.style.ERROR("Error: Invalid username"))
            return
        if not re.match(
                "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%*&]).{7,56})",
                data.get('password')):
            self.stdout.write(self.style.ERROR("Error: Invalid password"))
            return

        user = User.objects.filter(username=options['created_by']).first()
        if not user:
            self.stdout.write(
                self.style.ERROR("Error: You can not create user"))
            return
        existing_user = User.objects.filter(
            username=options['username']).first()
        if existing_user:
            self.stdout.write(self.style.ERROR("Error: User already exists"))
            return

        if user and not existing_user:
            new_user = User.objects.create_user(
                data['username'], data['email'], data['password'])
            new_user.save()
            new_api_user = ApiUser(user=new_user, created_by=user)
            new_api_user.save()
            self.stdout.write(self.style.SUCCESS("Successfully created user"))
            return
            self.stdout.write(self.style.ERROR("Error: User not created"))
        self.stdout.write(self.style.ERROR("Error: Invalid Data"))

#!/usr/bin/env bash

python manage.py shell -c "
import os
from django.contrib.auth.models import User

username = os.environ.get('CAMPUSHIRE_LOGIN_USERNAME')
password = os.environ.get('CAMPUSHIRE_LOGIN_PASSWORD')

if username and password:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': 'rakshitapatil@gmail.com'}
    )

    user.set_password(password)
    user.save()

    print('CampusHire login account ready.')
"

python manage.py seed_jobs

gunicorn config.wsgi:application

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

python manage.py shell -c "
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute(
        \"SELECT setval(
            pg_get_serial_sequence('recruiters_recruiter', 'id'),
            COALESCE((SELECT MAX(id) FROM recruiters_recruiter), 1),
            true
        )\"
    )

print('Recruiter ID sequence fixed.')
"

gunicorn config.wsgi:application
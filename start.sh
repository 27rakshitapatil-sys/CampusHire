#!/usr/bin/env bash
python manage.py seed_jobs
gunicorn config.wsgi:application
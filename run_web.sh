#!/bin/sh

# wait for PSQL server to start
sleep 10

# prepare init migration
# su -m electron -c "python manage.py makemigrations"  
python manage.py makemigrations

# migrate db, so we have the latest db schema
# su -m electron -c "python manage.py migrate"  
python manage.py migrate

# start server on public ip interface, on port 8000
# su -m electron -c "python manage.py runserver 0.0.0.0:8000"  
gunicorn --workers 4 --bind 0.0.0.0:8000 --reload --log-level info \
        --access-logfile ./logs/web_access.log --error-logfile ./logs/web_error.log mhtportal.wsgi
#!/usr/bin/env bash
# Exit on error
#!/usr/bin/env bash
set -o errexit

echo "===> Installing dependencies"
pip install -r requirements.txt

echo "===> Collecting static files"
python manage.py collectstatic --no-input

echo "===> Making migrations"
python manage.py makemigrations

echo "===> Applying migrations"
python manage.py migrate

echo "===> Verifying DB state"
python manage.py shell << END
from django.db import connection
print("ENGINE:", connection.settings_dict["ENGINE"])
print("DB NAME:", connection.settings_dict["NAME"])
with connection.cursor() as cursor:
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    print("Tables:", cursor.fetchall())
END

echo "===> Creating superuser"
python manage.py shell << END
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "adminpass")
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
END

echo "===> Starting server"
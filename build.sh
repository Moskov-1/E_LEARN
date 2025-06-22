#!/usr/bin/env bash
# Exit on error
echo "===> Running build.sh"
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

echo "Using DB URL: $DATABASE_URL"
python manage.py dbshell -c "SELECT current_database();"
# Apply any outstanding database migrations
python manage.py makemigrations
echo "===> Running migrations"

python manage.py migrate
echo "===> Done with migrations"

echo "===> Creating superuser if not exists"

# Create superuser from env vars
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
email = "${DJANGO_SUPERUSER_EMAIL}"
username = "${DJANGO_SUPERUSER_USERNAME}"
password = "${DJANGO_SUPERUSER_PASSWORD}"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)

from django.db import connection
print("ENGINE:", connection.settings_dict["ENGINE"])
print("NAME:", connection.settings_dict["NAME"])
END

python manage.py dbshell -c "\dt"
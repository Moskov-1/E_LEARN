# go to gmail > security > enable 2 step verification if disabled
# go to search bar > app password > create app > copy password > paste here
from decouple import config

ENVIRONMENT = config('ENVIRONMENT')
SECRET_KEY = config('SECRET_KEY')


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT', cast=int)

# Database settings
MYSQL_USER=config('MYSQL_USER')
MYSQL_PASSWORD=config('MYSQL_PASSWORD')

# Posgrate settings 
# is in settins.py DATABASES
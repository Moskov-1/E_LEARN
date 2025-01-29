from django.conf import settings

def site_info(request):
    return {
        'site_info': settings.SITE_INFO
    }
from django.conf import settings


def site_settings(request):
    return {
        "contact_email": settings.CONTACT_EMAIL,
        "instagram_url": settings.INSTAGRAM_URL,
    }

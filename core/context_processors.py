from django.conf import settings

def direction(request):
    return {
        'is_rtl' : request.LANGUAGE_CODE in settings.RTL_LANGUAGES
    }
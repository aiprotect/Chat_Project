from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),  # مسیر chat/ را برگرداندیم
    path('', include('chat.urls')),
    path('', include('index.urls')),
    path('', include('accounts.urls')),
    prefix_default_language=True
)
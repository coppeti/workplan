from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('calplan.urls')),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('accounts/', include('django.contrib.auth.urls')),
    path('event/', include('events.urls')),
    path('mgmt/', admin.site.urls),
]

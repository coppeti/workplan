from django.contrib import admin
from django.urls import path, include

from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

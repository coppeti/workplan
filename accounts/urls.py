from django.urls import path
from .views import signup
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', signup, name='signup'),
]
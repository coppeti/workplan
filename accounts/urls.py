from django.urls import path
from .views import signup

from .views import ActivateAccount

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]
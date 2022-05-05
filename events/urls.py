from django.urls import path

from .views import EventIndex, NewEvent, EditEvent, DelEvent

urlpatterns = [
    path('', EventIndex.as_view(), name='event_index'),
    path('new-event/', NewEvent.as_view(), name='new_event'),
    path('edit-event/<int:pk>/', EditEvent.as_view(), name='edit_event'),
    path('del-event/<int:pk>/', DelEvent.as_view(), name='del_event'),
]
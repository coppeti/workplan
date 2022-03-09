from django.urls import path

from .views import WorkplanIndex, NewActivity, EditActivity

urlpatterns = [
    path('', WorkplanIndex.as_view(), name='workplan_index'),
    path('new-activity/', NewActivity.as_view(), name='new_activity'),
    path('edit-activity/<int:pk>', EditActivity.as_view(), name='edit_activity'),
]
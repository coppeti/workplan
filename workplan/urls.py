from django.urls import path

from config.utils import a_year
from .views import WorkplanIndex, NewActivity, EditActivity, Holidays

urlpatterns = [
    path('', WorkplanIndex.as_view(), name='workplan_index'),
    path('holidays/<int:year>/<str:region>', Holidays.as_view(), name='holidays'),
    path('new-activity/', NewActivity.as_view(), name='new_activity'),
    path('edit-activity/<int:pk>', EditActivity.as_view(), name='edit_activity'),
]
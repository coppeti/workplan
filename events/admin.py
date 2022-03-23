from django.contrib import admin
from .models import Activity, Event, Diary


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "activity_id",
        "date_start",
        "date_stop",
        "confirmed",
        "is_active",
    )
    list_editable = (
        "confirmed",
        "is_active",
    )
    list_filter = (
        "user_id",
        "activity_id",
        "confirmed",
        "is_active",
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_name",
    )


admin.site.register(Diary)

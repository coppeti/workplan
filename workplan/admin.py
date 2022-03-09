from django.contrib import admin
from .models import Activities, Planning, Diary


@admin.register(Planning)
class PlanningAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "activity_id",
        "date_start",
        "date_stop",
        "confirmed",
        "is_active",
    )
    list_filter = (
        "user_id",
        "activity_id",
        "confirmed",
        "is_active",
    )


admin.site.register(Activities)
admin.site.register(Diary)

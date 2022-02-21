from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'username',)
    list_display_links = ('last_name', 'first_name', 'username',)
    search_fields = ('last_name', 'username',)
    list_filter = ('last_name', 'username',)

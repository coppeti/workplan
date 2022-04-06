from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('upper_last_name', 'title_first_name', 'username',)
    list_display_links = ('upper_last_name', 'title_first_name', 'username',)
    search_fields = ('last_name', 'username',)
    list_filter = ('last_name', 'username',)
    ordering = ('last_name',)

    @admin.display(description='Lastname upper')
    def upper_last_name(self, obj):
        return f'{obj.last_name.upper()}'

    @admin.display(description='Firstname title')
    def title_first_name(self, obj):
        return f'{obj.first_name.title()}'


admin.site.register(User, UserAdmin)

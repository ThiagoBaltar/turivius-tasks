from django.contrib import admin

from .models import UserTask


@admin.register(UserTask)
class BrokenBoletoAdmin(admin.ModelAdmin):
    list_display = (
        'uuid', 'user', 'title', 'description', 'created_at', 'updated_at'
    )
    list_select_related = ('user',)
    ordering = ('-created_at',)

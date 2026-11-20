from django.contrib import admin

from core.models import UserMeta


@admin.register(UserMeta)
class UserMetaAdmin(admin.ModelAdmin):
    list_display = ("user", "verified", "free_access", "daily_word_goal")
    list_editable = ("verified", "free_access")
    search_fields = ("user__email", "user__username")

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from api import models


class VotingUserInline(admin.StackedInline):
    model = models.VotingUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [VotingUserInline]


admin.site.register(models.Generation)
admin.site.register(models.Artist)
admin.site.register(models.Art)
admin.site.register(models.Vote)
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

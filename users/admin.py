from edesia.users.models import UserProfile
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)

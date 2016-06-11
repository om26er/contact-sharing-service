from django.contrib import admin
from django.contrib.auth.models import Group

from contact_share_service.models import User


class UserAdmin(admin.ModelAdmin):
    fields = (
        'is_active',
        'email',
        'password',
        'full_name',
    )

    class Meta:
        model = User


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

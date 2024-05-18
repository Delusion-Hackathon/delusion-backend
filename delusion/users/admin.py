from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from delusion.users.models import CompanyRegistration, Country, User, MeshUser


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'msp_name'
        )
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info', {
            'fields': ('msp_name', 'profile_picture'),
        }),
    )


admin.site.register(CompanyRegistration)
admin.site.register(Country)
admin.site.register(MeshUser)

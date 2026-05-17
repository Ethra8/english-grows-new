from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'billing_email',
        'phone_number',
        'country',
        'created_at',
    )

    search_fields = (
        'name',
        'billing_email',
        'tax_id',
    )

    list_filter = (
        'country',
        'created_at',
    )


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

    fields = (
        'company',
        'role',
        'country',
        'level',
    )


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'get_company',
        'get_role',
        'is_staff',
    )

    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'groups',
        'profile__role',
        'profile__company',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'profile__company__name',
    )

    def get_company(self, obj):
        if hasattr(obj, 'profile') and obj.profile.company:
            return obj.profile.company.name
        return '-'

    get_company.short_description = 'Company'
    get_company.admin_order_field = 'profile__company__name'

    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.get_role_display()
        return '-'

    get_role.short_description = 'Role'
    get_role.admin_order_field = 'profile__role'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
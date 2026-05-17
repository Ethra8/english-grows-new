from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Company, UserProfile


User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0

    fields = (
        'company',
        'role',
        'country',
        'level',
        'created_at',
        'updated_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'get_role',
        'get_company',
        'is_staff',
        'is_active',
    )

    list_select_related = (
        'profile',
        'profile__company',
    )

    def get_role(self, obj):
        if hasattr(obj, 'profile') and obj.profile.role:
            return obj.profile.get_role_display()
        return '-'

    get_role.short_description = 'Role'

    def get_company(self, obj):
        if hasattr(obj, 'profile') and obj.profile.company:
            return obj.profile.company.name
        return '-'

    get_company.short_description = 'Company'


class CompanyUserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 0
    can_delete = False

    fields = (
        'user',
        'get_first_name',
        'get_last_name',
        'get_email',
        'role',
        'level',
        'country',
    )

    readonly_fields = (
        'user',
        'get_first_name',
        'get_last_name',
        'get_email',
    )

    def get_first_name(self, obj):
        return obj.user.first_name or '-'

    get_first_name.short_description = 'First name'

    def get_last_name(self, obj):
        return obj.user.last_name or '-'

    get_last_name.short_description = 'Last name'

    def get_email(self, obj):
        return obj.user.email or '-'

    get_email.short_description = 'Email'


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tax_id',
        'billing_email',
        'phone_number',
        'country',
        'get_number_of_users',
        'created_at',
    )

    search_fields = (
        'name',
        'tax_id',
        'billing_email',
        'phone_number',
        'user_profiles__user__username',
        'user_profiles__user__first_name',
        'user_profiles__user__last_name',
        'user_profiles__user__email',
    )

    list_filter = (
        'country',
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )

    inlines = (
        CompanyUserProfileInline,
    )

    def get_number_of_users(self, obj):
        return obj.user_profiles.count()

    get_number_of_users.short_description = 'Users'


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'get_first_name',
        'get_last_name',
        'get_email',
        'role',
        'company',
        'level',
        'country',
        'created_at',
    )

    list_filter = (
        'role',
        'level',
        'company',
        'country',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
        'company__name',
    )

    list_select_related = (
        'user',
        'company',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    def get_first_name(self, obj):
        return obj.user.first_name or '-'

    get_first_name.short_description = 'First name'

    def get_last_name(self, obj):
        return obj.user.last_name or '-'

    get_last_name.short_description = 'Last name'

    def get_email(self, obj):
        return obj.user.email or '-'

    get_email.short_description = 'Email'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Company, CompanyAdmin)
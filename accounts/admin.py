from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, NutritionProfile, EmailConfirmation


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'is_staff', 'is_active')

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'bio')
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')


@admin.register(NutritionProfile)
class NutritionProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'goal')
    list_filter = ('gender', 'goal')


admin.site.register(EmailConfirmation)

admin.site.site_header = "DietSync Administration"
admin.site.site_title = "DietSync Admin"
admin.site.index_title = "Welcome to DietSync Dashboard"
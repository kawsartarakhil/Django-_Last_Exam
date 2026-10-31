from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,NutritionProfile

admin.site.register(NutritionProfile)
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = ("username","is_active","is_staff")
    list_filter = ("first_name","last_name")
    search_fields = ("email","fist_name","last_name")
    ordering = ("email",)

    fieldsets = (
        (None,{"fields":("email","password")}),
        ("Personal info",{"fields":("first_name","last_name")}),
        ("Permissions",{"fields":("is_active","is_staff","is_superuser")}),
        ("Important dates",{"fields":("last_login","date_joined")})
    )

    add_fieldsets = (
        (None,{
            "classes":("wide",),
            "fields":("email","password1","password2","is_staff","is_active")
        })
    )


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, ConfirmationCode

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "username", "full_name", "birth_date", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "username", "full_name")
    ordering = ("id",)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_staff', 'is_active')}),
        ('Personal info', {'fields': ('username', 'full_name', 'birth_date')}),
        ('Date information', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'birth_date', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "code", "created_at"]
    search_fields = ["user__email", "code"]

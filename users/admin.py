from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, EmailCode


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_fields = ("created_at", "updated_at")
    list_display = (
        "email", "username", "is_staff", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_active", "is_superuser")
    fieldsets = (
        ('Personal Information', {
         "fields": ("email", "username", "fullname", "photo", "password")}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Date and Time", {
         "fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        ('Personal Information', {
            "classes": ("wide",),
            "fields": ("email", "username", "fullname", "photo", "password1", "password2")}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    search_fields = ("email",)
    ordering = ("email",)


class EmailCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "updated_at", "status")
    list_filter = ("status",)
    search_fields = ("user",)
    ordering = ("-updated_at",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(EmailCode, EmailCodeAdmin)

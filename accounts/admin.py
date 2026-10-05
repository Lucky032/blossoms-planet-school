from django.contrib import admin
from .models import UserProfile, PasswordResetOTP


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "phone",
    )

    search_fields = (
        "user__username",
        "role",
    )



@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "otp",
        "created_at",
        "expires_at",
        "is_used",
        "attempts",
    )

    list_filter = (
        "is_used",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
    )
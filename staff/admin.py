from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "first_name",
        "role",
        "phone",
        "is_active",
    )

    list_filter = (
        "role",
        "gender",
        "is_active",
    )

    search_fields = (
        "employee_id",
        "first_name",
        "last_name",
        "phone",
    )

    list_editable = (
        "is_active",
    )
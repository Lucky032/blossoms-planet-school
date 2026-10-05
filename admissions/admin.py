from django.contrib import admin
from .models import AdmissionEnquiry


@admin.register(AdmissionEnquiry)
class AdmissionEnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "student_name",
        "parent_name",
        "phone",
        "applying_for_class",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "gender",
        "applying_for_class",
    )

    search_fields = (
        "student_name",
        "parent_name",
        "phone",
        "email",
    )

    list_editable = (
        "status",
    )

    ordering = (
        "-created_at",
    )
from django.contrib import admin
from .models import SchoolProfile, Facility, Statistic


@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "phone_primary",
        "email",
        "opening_time",
        "closing_time",
    )

    search_fields = (
        "name",
        "city",
        "email",
    )

    list_filter = (
        "city",
        "state",
    )

    ordering = ("name",)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    ordering = (
        "display_order",
    )

    search_fields = (
        "title",
    )

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "value",
        "suffix",
        "display_order",
        "is_active",
    )

    list_editable = (
        "value",
        "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "display_order",
    )

    search_fields = (
        "title",
    )
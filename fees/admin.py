from django.contrib import admin

from .models import FeeCollection, FeeStructure


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):

    list_display = (
        "school_class",
        "fee_type",
        "amount",
        "created_at",
    )

    search_fields = (
        "fee_type",
        "school_class__name",
    )

    list_filter = (
        "school_class",
        "fee_type",
    )

    ordering = (
        "fee_type",
    )


@admin.register(FeeCollection)
class FeeCollectionAdmin(admin.ModelAdmin):

    list_display = (
        "receipt_number",
        "student",
        "fee_structure",
        "amount_paid",
        "payment_mode",
        "payment_date",
    )

    search_fields = (
        "receipt_number",
        "student__first_name",
        "student__last_name",
    )

    list_filter = (
        "payment_mode",
        "payment_date",
        "fee_structure",
    )

    date_hierarchy = "payment_date"

    ordering = (
        "-payment_date",
    )
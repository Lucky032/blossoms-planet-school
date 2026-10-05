from django.contrib import admin
from .models import GalleryImage, Event


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "display_order",
        "is_active",
    )

    list_editable = (
        "display_order",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "title",
    )

    ordering = (
        "display_order",
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "event_date",
        "venue",
        "is_active",
    )

    list_filter = (
        "is_active",
        "event_date",
    )

    search_fields = (
        "title",
        "venue",
    )

    ordering = (
        "-event_date",
    )
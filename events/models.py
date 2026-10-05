from django.db import models


class GalleryImage(models.Model):
    title = models.CharField(max_length=150)

    image = models.ImageField(
        upload_to="gallery/"
    )

    description = models.TextField(
        blank=True
    )

    display_order = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["display_order"]
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        return self.title

class Event(models.Model):

    title = models.CharField(
        max_length=200
    )

    event_date = models.DateField()

    event_time = models.TimeField()

    venue = models.CharField(
        max_length=200
    )

    description = models.TextField()

    cover_image = models.ImageField(
        upload_to="events/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-event_date"]

    def __str__(self):
        return self.title
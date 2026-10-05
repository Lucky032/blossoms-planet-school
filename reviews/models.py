from django.db import models


class Review(models.Model):

    name = models.CharField(
        max_length=100
    )

    designation = models.CharField(
        max_length=100,
        help_text="Example: Parent of Class V Student"
    )

    review = models.TextField()

    rating = models.PositiveSmallIntegerField(
        default=5
    )

    photo = models.ImageField(
        upload_to="reviews/",
        blank=True,
        null=True,
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
        ordering = [
            "display_order",
            "-created_at",
        ]

    def __str__(self):
        return self.name
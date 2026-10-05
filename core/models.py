from django.db import models


class SchoolProfile(models.Model):
    name = models.CharField(max_length=150)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    address = models.TextField()
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    phone_primary = models.CharField(max_length=15)
    phone_secondary = models.CharField(max_length=15, blank=True)

    email = models.EmailField()

    opening_time = models.TimeField()
    closing_time = models.TimeField()

    working_days = models.CharField(max_length=50)

    logo = models.ImageField(
        upload_to="school/logo/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "School Profile"
        verbose_name_plural = "School Profile"

    def __str__(self):
        return self.name
    
class Facility(models.Model):
    title = models.CharField(max_length=100)

    description = models.TextField()

    image = models.ImageField(
        upload_to="facilities/"
    )

    display_order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order"]
        verbose_name_plural = "Facilities"

    def __str__(self):
        return self.title
    
class Statistic(models.Model):
    title = models.CharField(max_length=100)

    value = models.PositiveIntegerField()

    icon = models.CharField(
        max_length=50,
        help_text="Example: 🎓 📚 👨‍🏫 🏆"
    )

    suffix = models.CharField(
        max_length=10,
        default="+",
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

    def __str__(self):
        return self.title
print("Statistic loaded successfully")

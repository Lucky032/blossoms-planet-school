from django.db import models
from datetime import date


class Staff(models.Model):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    ROLE_CHOICES = (
        ("Principal", "Principal"),
        ("Vice Principal", "Vice Principal"),
        ("Teacher", "Teacher"),
        ("Accountant", "Accountant"),
        ("Librarian", "Librarian"),
        ("Office Staff", "Office Staff"),
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
    )

    qualification = models.CharField(
        max_length=200,
        blank=True,
    )

    experience = models.PositiveIntegerField(
        default=0,
        help_text="Experience in years",
    )

    phone = models.CharField(
        max_length=15,
        unique=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
        unique=True,
    )

    joining_date = models.DateField()

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    photo = models.ImageField(
        upload_to="staff_photos/",
        blank=True,
        null=True,
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    address = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["employee_id"]
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"
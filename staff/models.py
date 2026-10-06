from django.db import models
from datetime import date
from django.contrib.auth.models import User


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

    user = models.OneToOneField(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="staff_profile",
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

class StaffAttendance(models.Model):

    STATUS_CHOICES = (
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Leave", "Leave"),
    )

    LEAVE_TYPE_CHOICES = (
        ("Paid", "Paid Leave"),
        ("Unpaid", "Unpaid Leave"),
    )

    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="attendance",
    )

    date = models.DateField(
        default=date.today,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )

    leave_type = models.CharField(
        max_length=10,
        choices=LEAVE_TYPE_CHOICES,
        blank=True,
        null=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    recorded_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff_attendance_records",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-date", "staff__employee_id"]
        unique_together = ("staff", "date")

    def __str__(self):
        return f"{self.staff.employee_id} - {self.date} - {self.status}"
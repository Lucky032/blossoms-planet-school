from django.db import models

# Create your models here.
from django.db import models

from academics.models import Student

from django.contrib.auth import get_user_model

User = get_user_model()


class Attendance(models.Model):

    STATUS_CHOICES = [

        ("Present", "Present"),

        ("Absent", "Absent"),

    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Present",
    )

    remarks = models.TextField(
        blank=True,
        null=True,
    )

    recorded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        ordering = ["-date", "student__first_name"]

        constraints = [

            models.UniqueConstraint(
                fields=["student", "date"],
                name="unique_student_attendance",
            )

        ]

    def __str__(self):

        return f"{self.student} - {self.date} - {self.status}"
from django.db import models
from staff.models import Staff


class AdmissionEnquiry(models.Model):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    STATUS_CHOICES = (
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Interested", "Interested"),
        ("Admission Completed", "Admission Completed"),
        ("Rejected", "Rejected"),
    )

    student_name = models.CharField(max_length=150)

    parent_name = models.CharField(max_length=150)

    phone = models.CharField(max_length=15)

    email = models.EmailField(blank=True)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    applying_for_class = models.CharField(max_length=50)

    address = models.TextField()

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default="New"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Admission Enquiry"
        verbose_name_plural = "Admission Enquiries"

    def __str__(self):
        return f"{self.student_name} - {self.parent_name}"
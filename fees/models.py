from django.db import models
from academics.models import Student, SchoolClass


# ==========================
# Fee Structure
# ==========================

class FeeStructure(models.Model):

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="fee_structures",
        null=True,
        blank=True,
    )

    FEE_TYPE_CHOICES = (
        ("Admission", "Admission"),
        ("Tuition", "Tuition"),
        ("Transport", "Transport"),
        ("Library", "Library"),
        ("Exam", "Exam"),
        ("Lab", "Lab"),
        ("Sports", "Sports"),
        ("Other", "Other"),
    )

    fee_type = models.CharField(
        max_length=30,
        choices=FEE_TYPE_CHOICES,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    description = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["fee_type"]

    def __str__(self):
        return f"{self.school_class} - {self.fee_type}"


# ==========================
# Fee Collection
# ==========================

class FeeCollection(models.Model):

    PAYMENT_MODE_CHOICES = (
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Debit Card", "Debit Card"),
        ("Bank Transfer", "Bank Transfer"),
    )

    PAYMENT_STATUS_CHOICES = (
        ("SUCCESS", "Success"),
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="fee_collections",
    )

    fee_structure = models.ForeignKey(
        FeeStructure,
        on_delete=models.CASCADE,
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    fine = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    payment_mode = models.CharField(
        max_length=30,
        choices=PAYMENT_MODE_CHOICES,
    )

    payment_date = models.DateField()

    receipt_number = models.CharField(
        max_length=30,
        unique=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    # ==========================
    # Online Payment Details
    # ==========================

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="SUCCESS",
    )

    order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    gateway_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    gateway_response = models.JSONField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-payment_date"]

    def __str__(self):
        return self.receipt_number
from django.db import models
from staff.models import Staff


class AcademicYear(models.Model):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    name = models.CharField(max_length=50)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.name


class Section(models.Model):
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name="sections"
    )

    name = models.CharField(max_length=10)

    class Meta:
        unique_together = ("school_class", "name")
        ordering = ["school_class", "name"]

    def __str__(self):
        return f"{self.school_class} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    admission_number = models.CharField(
        max_length=20,
        unique=True
    )

    # ⭐ NEW FIELD
    photo = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="students"
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT,
        related_name="students"
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        related_name="students"
    )

    father_name = models.CharField(max_length=150)

    mother_name = models.CharField(
        max_length=150,
        blank=True
    )

    phone = models.CharField(max_length=15)

    email = models.EmailField(blank=True)

    address = models.TextField()

    admission_date = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["admission_number"]

    def __str__(self):
        return f"{self.admission_number} - {self.first_name}"


class TeacherAssignment(models.Model):

    teacher = models.ForeignKey(
        Staff,
        on_delete=models.PROTECT,
        related_name="teaching_assignments",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="teacher_assignments",
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT,
        related_name="teacher_assignments",
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        related_name="teacher_assignments",
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="teacher_assignments",
    )

    class Meta:
        unique_together = (
            "teacher",
            "subject",
            "school_class",
            "section",
            "academic_year",
        )

        ordering = (
            "school_class",
            "section",
        )

    def __str__(self):
        return (
            f"{self.teacher} - "
            f"{self.subject} - "
            f"{self.school_class}-{self.section.name}"
        )
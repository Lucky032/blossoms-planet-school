from django.db import models
from academics.models import AcademicYear, SchoolClass, Subject
from academics.models import Student


class Exam(models.Model):
    TERM_CHOICES = [
        ("TERM1", "Term 1"),
        ("TERM2", "Term 2"),
        ("TERM3", "Term 3"),
    ]

    name = models.CharField(max_length=100)
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name="exams"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    term = models.CharField(max_length=20, choices=TERM_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


class Grade(models.Model):
    grade_name = models.CharField(max_length=10)
    minimum_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    maximum_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["-minimum_percentage"]

    def __str__(self):
        return self.grade_name


class ExamSubject(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )
    maximum_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=35)

    class Meta:
        unique_together = ("exam", "school_class", "subject")

    def __str__(self):
        return f"{self.exam} - {self.subject}"


class StudentMark(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="marks",
    )
    exam_subject = models.ForeignKey(
        ExamSubject,
        on_delete=models.CASCADE,
        related_name="student_marks",
    )
    obtained_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    remarks = models.CharField(
        max_length=255,
        blank=True
    )

    class Meta:
        unique_together = ("student", "exam_subject")

    def __str__(self):
        return f"{self.student} - {self.exam_subject}"

class StudentResult(models.Model):
    RESULT_CHOICES = [
        ("PASS", "Pass"),
        ("FAIL", "Fail"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="results",
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="results",
    )

    total_marks = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    rank = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES,
        default="PASS",
    )

    class Meta:
        unique_together = ("student", "exam")
        ordering = ["rank", "-percentage"]

    def __str__(self):
        return f"{self.student} - {self.exam}"
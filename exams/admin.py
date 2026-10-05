from django.contrib import admin
from .models import Exam, Grade, ExamSubject, StudentMark, StudentResult



@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "academic_year",
        "term",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = (
        "academic_year",
        "term",
        "is_active",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = ("-start_date",)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "grade_name",
        "minimum_percentage",
        "maximum_percentage",
    )
    ordering = ("-minimum_percentage",)


@admin.register(ExamSubject)
class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = (
        "exam",
        "school_class",
        "subject",
        "maximum_marks",
        "passing_marks",
    )
    list_filter = (
        "exam",
        "school_class",
    )
    search_fields = (
        "subject__name",
    )


@admin.register(StudentMark)
class StudentMarkAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "exam_subject",
        "obtained_marks",
    )
    list_filter = (
        "exam_subject__exam",
    )
    search_fields = (
        "student__first_name",
        "student__last_name",
    )

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "exam",
        "total_marks",
        "percentage",
        "grade",
        "rank",
        "result",
    )

    list_filter = (
        "exam",
        "result",
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
    )

    ordering = (
        "rank",
    )
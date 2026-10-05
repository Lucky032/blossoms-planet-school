from decimal import Decimal

from .models import Grade, StudentMark, StudentResult


class ResultService:

    @staticmethod
    def calculate_student_result(student, exam):

        marks = (
            StudentMark.objects.filter(
                student=student,
                exam_subject__exam=exam,
            )
            .select_related("exam_subject")
        )

        if not marks.exists():
            return None

        total_obtained = Decimal("0")
        total_maximum = Decimal("0")
        is_pass = True

        for mark in marks:

            total_obtained += mark.obtained_marks
            total_maximum += Decimal(mark.exam_subject.maximum_marks)

            if mark.obtained_marks < mark.exam_subject.passing_marks:
                is_pass = False

        percentage = (
            (total_obtained / total_maximum) * 100
            if total_maximum > 0
            else Decimal("0")
        )

        grade = Grade.objects.filter(
            minimum_percentage__lte=percentage,
            maximum_percentage__gte=percentage,
        ).first()

        result, created = StudentResult.objects.update_or_create(
            student=student,
            exam=exam,
            defaults={
                "total_marks": total_obtained,
                "percentage": percentage,
                "grade": grade,
                "result": "PASS" if is_pass else "FAIL",
            },
        )

        ResultService.calculate_rankings(
            exam,
            student.school_class,
        )

        return result

    @staticmethod
    def calculate_rankings(exam, school_class):

        results = (
            StudentResult.objects.filter(
                exam=exam,
                student__school_class=school_class,
            )
            .select_related("student")
            .order_by(
                "-percentage",
                "-total_marks",
                "student__admission_number",
            )
        )

        current_rank = 1
        previous_percentage = None

        for index, result in enumerate(results, start=1):

            if previous_percentage is None:
                current_rank = 1

            elif result.percentage != previous_percentage:
                current_rank = index

            result.rank = current_rank
            result.save(update_fields=["rank"])

            previous_percentage = result.percentage
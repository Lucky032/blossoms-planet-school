from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F, Avg

from academics.models import Student

from .models import (
    Exam,
    Grade,
    ExamSubject,
    StudentMark,
    StudentResult,
)

from .forms import (
    ExamForm,
    GradeForm,
    ExamSubjectForm,
    StudentMarkForm,
    StudentMarkEditForm,
    MarksEntryFilterForm,
    RankingFilterForm,
)

from .services import ResultService

from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_roles
from academics.models import Student, TeacherAssignment, Section



# =========================
# EXAM CRUD
# =========================

@login_required
@allowed_roles("Admin", "Principal")
def exam_list(request):

    search = request.GET.get("search", "")

    exams = Exam.objects.all()

    if search:
        exams = exams.filter(
            Q(name__icontains=search)
            | Q(academic_year__name__icontains=search)
        )

    paginator = Paginator(exams, 10)
    page = request.GET.get("page")

    context = {
        "exams": paginator.get_page(page),
        "search": search,
    }

    return render(
        request,
        "exams/exam_list.html",
        context,
    )


@login_required
@allowed_roles("Admin", "Principal")
def exam_create(request):

    if request.method == "POST":

        form = ExamForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Exam created successfully.",
            )

            return redirect("exam_list")

    else:

        form = ExamForm()

    return render(
        request,
        "exams/exam_form.html",
        {
            "form": form,
            "title": "Add Exam",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def exam_update(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk,
    )

    if request.method == "POST":

        form = ExamForm(
            request.POST,
            instance=exam,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Exam updated successfully.",
            )

            return redirect("exam_list")

    else:

        form = ExamForm(
            instance=exam,
        )

    return render(
        request,
        "exams/exam_form.html",
        {
            "form": form,
            "title": "Edit Exam",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def exam_delete(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk,
    )

    if request.method == "POST":

        exam.delete()

        messages.success(
            request,
            "Exam deleted successfully.",
        )

        return redirect("exam_list")

    return render(
        request,
        "exams/exam_delete.html",
        {
            "exam": exam,
        },
    )

# =====================================
# GRADE CRUD
# =====================================

@login_required
@allowed_roles("Admin", "Principal")
def grade_list(request):

    search = request.GET.get("search", "")

    grades = Grade.objects.all()

    if search:
        grades = grades.filter(
            grade_name__icontains=search
        )

    paginator = Paginator(grades, 10)
    page = request.GET.get("page")

    context = {
        "grades": paginator.get_page(page),
        "search": search,
    }

    return render(
        request,
        "exams/grade_list.html",
        context,
    )


@login_required
@allowed_roles("Admin", "Principal")
def grade_create(request):

    if request.method == "POST":

        form = GradeForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Grade created successfully.",
            )

            return redirect("grade_list")

    else:

        form = GradeForm()

    return render(
        request,
        "exams/grade_form.html",
        {
            "form": form,
            "title": "Add Grade",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def grade_update(request, pk):

    grade = get_object_or_404(
        Grade,
        pk=pk,
    )

    if request.method == "POST":

        form = GradeForm(
            request.POST,
            instance=grade,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Grade updated successfully.",
            )

            return redirect("grade_list")

    else:

        form = GradeForm(
            instance=grade,
        )

    return render(
        request,
        "exams/grade_form.html",
        {
            "form": form,
            "title": "Edit Grade",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def grade_delete(request, pk):

    grade = get_object_or_404(
        Grade,
        pk=pk,
    )

    if request.method == "POST":

        grade.delete()

        messages.success(
            request,
            "Grade deleted successfully.",
        )

        return redirect("grade_list")

    return render(
        request,
        "exams/grade_delete.html",
        {
            "grade": grade,
        },
    )
# =====================================
# EXAM SUBJECT CRUD
# =====================================

@login_required
@allowed_roles("Admin", "Principal")
def exam_subject_list(request):

    search = request.GET.get("search", "")

    subjects = ExamSubject.objects.select_related(
        "exam",
        "school_class",
        "subject",
    )

    if search:
        subjects = subjects.filter(
            Q(exam__name__icontains=search)
            | Q(subject__name__icontains=search)
        )

    paginator = Paginator(subjects, 10)
    page = request.GET.get("page")

    return render(
        request,
        "exams/exam_subject_list.html",
        {
            "subjects": paginator.get_page(page),
            "search": search,
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def exam_subject_create(request):

    if request.method == "POST":

        form = ExamSubjectForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Exam subject added successfully.",
            )

            return redirect("exam_subject_list")

    else:

        form = ExamSubjectForm()

    return render(
        request,
        "exams/exam_subject_form.html",
        {
            "form": form,
            "title": "Add Exam Subject",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def exam_subject_update(request, pk):

    obj = get_object_or_404(
        ExamSubject,
        pk=pk,
    )

    if request.method == "POST":

        form = ExamSubjectForm(
            request.POST,
            instance=obj,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Exam subject updated successfully.",
            )

            return redirect("exam_subject_list")

    else:

        form = ExamSubjectForm(
            instance=obj,
        )

    return render(
        request,
        "exams/exam_subject_form.html",
        {
            "form": form,
            "title": "Edit Exam Subject",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def exam_subject_delete(request, pk):

    obj = get_object_or_404(
        ExamSubject,
        pk=pk,
    )

    if request.method == "POST":

        obj.delete()

        messages.success(
            request,
            "Exam subject deleted successfully.",
        )

        return redirect("exam_subject_list")

    return render(
        request,
        "exams/exam_subject_delete.html",
        {
            "exam_subject": obj,
        },
    )

from django.db import transaction


from django.db import transaction

@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def marks_entry(request):

    form = MarksEntryFilterForm(
        request.GET or None,
        user=request.user,
    )

    students = []
    exam_subject = None

    # ==========================================
    # POST - SAVE MARKS
    # ==========================================
    if request.method == "POST":

        exam_subject = get_object_or_404(
            ExamSubject,
            pk=request.POST.get("exam_subject_id"),
        )

        # ==========================================
        # TEACHER ACCESS CONTROL
        # ==========================================
        if request.user.userprofile.role == "Teacher":

            has_assignment = TeacherAssignment.objects.filter(
                teacher__user=request.user,
                subject=exam_subject.subject,
                school_class=exam_subject.school_class,
                academic_year=exam_subject.exam.academic_year,
            ).exists()

            if not has_assignment:

                messages.error(
                    request,
                    "You are not assigned to this subject and class."
                )

                return redirect("marks_entry")

        students = (
            Student.objects.filter(
                school_class=exam_subject.school_class,
                academic_year=exam_subject.exam.academic_year,
                is_active=True,
            )
            .select_related("section")
            .prefetch_related("marks")
            .order_by(
                "section__name",
                "admission_number",
            )
        )

        # ==========================================
        # TEACHER → ONLY ASSIGNED SECTION STUDENTS
        # ==========================================
        if request.user.userprofile.role == "Teacher":

            students = students.filter(
                section__teacher_assignments__teacher__user=request.user,
                section__teacher_assignments__subject=exam_subject.subject,
                section__teacher_assignments__academic_year=exam_subject.exam.academic_year,
            ).distinct()

        with transaction.atomic():

            for student in students:

                marks = request.POST.get(
                    f"marks_{student.id}"
                )

                if marks is None or marks == "":
                    continue

                StudentMark.objects.update_or_create(
                    student=student,
                    exam_subject=exam_subject,
                    defaults={
                        "obtained_marks": marks,
                    },
                )

                ResultService.calculate_student_result(
                    student,
                    exam_subject.exam,
                )

        messages.success(
            request,
            "Marks saved successfully."
        )

        return redirect(
            f"{request.path}"
            f"?exam={exam_subject.exam.id}"
            f"&school_class={exam_subject.school_class.id}"
            f"&subject={exam_subject.subject.id}"
        )

    # ==========================================
    # GET - LOAD STUDENTS
    # ==========================================
    if form.is_valid():

        exam = form.cleaned_data["exam"]
        school_class = form.cleaned_data["school_class"]
        subject = form.cleaned_data["subject"]

        # ==========================================
        # TEACHER → EXAM SUBJECT ACCESS CONTROL
        # ==========================================
        if request.user.userprofile.role == "Teacher":

            exam_subject = ExamSubject.objects.filter(
                exam=exam,
                school_class=school_class,
                subject=subject,
                exam__academic_year__in=TeacherAssignment.objects.filter(
                    teacher__user=request.user,
                    subject=subject,
                    school_class=school_class,
                ).values_list(
                    "academic_year",
                    flat=True,
                ),
            ).first()

        else:

            exam_subject = ExamSubject.objects.filter(
                exam=exam,
                school_class=school_class,
                subject=subject,
            ).first()

        if exam_subject:

            students = (
                Student.objects.filter(
                    school_class=school_class,
                    academic_year=exam.academic_year,
                    is_active=True,
                )
                .select_related("section")
                .prefetch_related("marks")
                .order_by(
                    "section__name",
                    "admission_number",
                )
            )

            # ==========================================
            # TEACHER → ONLY ASSIGNED SECTION STUDENTS
            # ==========================================
            if request.user.userprofile.role == "Teacher":

                students = students.filter(
                    section__teacher_assignments__teacher__user=request.user,
                    section__teacher_assignments__subject=subject,
                    section__teacher_assignments__academic_year=exam.academic_year,
                ).distinct()

    context = {
        "form": form,
        "students": students,
        "exam_subject": exam_subject,
    }

    return render(
        request,
        "exams/marks_entry.html",
        context,
    )

@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def student_mark_list(request):
    search = request.GET.get("search", "")

    marks = StudentMark.objects.select_related(
        "student",
        "exam_subject",
        "exam_subject__exam",
        "exam_subject__subject",
    )

    if search:
        marks = marks.filter(
            Q(student__first_name__icontains=search)
            | Q(student__last_name__icontains=search)
            | Q(student__admission_number__icontains=search)
            | Q(exam_subject__exam__name__icontains=search)
            | Q(exam_subject__subject__name__icontains=search)
        )

    paginator = Paginator(marks.order_by("student__admission_number"), 10)
    page = request.GET.get("page")

    context = {
        "marks": paginator.get_page(page),
        "search": search,
    }

    return render(
        request,
        "exams/student_mark_list.html",
        context,
    )

@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def student_mark_update(request, pk):
    mark = get_object_or_404(StudentMark, pk=pk)

    if request.method == "POST":
        form = StudentMarkEditForm(request.POST, instance=mark)

        if form.is_valid():
            form.save()

            ResultService.calculate_student_result(
                mark.student,
                mark.exam_subject.exam,
            )

            messages.success(
                request,
                "Student marks updated successfully.",
            )

            return redirect("student_mark_list")

    else:
        form = StudentMarkEditForm(instance=mark)

    return render(
        request,
        "exams/student_mark_form.html",
        {
            "form": form,
            "mark": mark,
            "title": "Edit Student Marks",
        },
    )

@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def student_mark_delete(request, pk):
    mark = get_object_or_404(StudentMark, pk=pk)

    if request.method == "POST":

        student = mark.student
        exam = mark.exam_subject.exam

        mark.delete()

        ResultService.calculate_student_result(
            student,
            exam,
        )

        messages.success(
            request,
            "Student marks deleted successfully.",
        )

        return redirect("student_mark_list")

    return render(
        request,
        "exams/student_mark_delete.html",
        {
            "mark": mark,
        },
    )


@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def class_ranking_list(request):

    form = RankingFilterForm(request.GET or None)

    rankings = StudentResult.objects.select_related(
        "student",
        "exam",
        "grade",
    )

    # ==========================================
    # TEACHER → ONLY ASSIGNED STUDENTS
    # ==========================================
    if request.user.userprofile.role == "Teacher":

        rankings = rankings.filter(
            student__section__teacher_assignments__teacher__user=request.user,
            student__section__teacher_assignments__academic_year=F(
                "exam__academic_year"
            ),
        ).distinct()

    # ==========================================
    # FILTERS
    # ==========================================
    if form.is_valid():

        exam = form.cleaned_data.get("exam")
        school_class = form.cleaned_data.get("school_class")

        if exam:
            rankings = rankings.filter(
                exam=exam,
            )

        if school_class:
            rankings = rankings.filter(
                student__school_class=school_class,
            )

    # ==========================================
    # ORDERING
    # ==========================================
    rankings = rankings.order_by(
        "rank",
        "-percentage",
        "-total_marks",
        "student__admission_number",
    )

    # ==========================================
    # SUMMARY STATISTICS
    # ==========================================
    total_students = rankings.count()

    pass_count = rankings.filter(
        result="PASS"
    ).count()

    fail_count = rankings.filter(
        result="FAIL"
    ).count()

    pass_percentage = (
        round(
            (pass_count / total_students) * 100,
            2,
        )
        if total_students > 0
        else 0
    )

    average_percentage = (
        round(
            sum(r.percentage for r in rankings) / total_students,
            2,
        )
        if total_students > 0
        else 0
    )

    topper = rankings.first()

    # ==========================================
    # PAGINATION
    # ==========================================
    paginator = Paginator(
        rankings,
        20,
    )

    page = request.GET.get("page")

    rankings = paginator.get_page(page)

    context = {
        "form": form,
        "rankings": rankings,

        "total_students": total_students,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "pass_percentage": pass_percentage,
        "average_percentage": average_percentage,
        "topper": topper,
    }

    return render(
        request,
        "exams/class_ranking_list.html",
        context,
    )

@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def result_analytics(request):

    results = StudentResult.objects.all()

    # ==========================================
    # TEACHER → ONLY ASSIGNED STUDENTS
    # ==========================================
    if request.user.userprofile.role == "Teacher":

        results = results.filter(
            student__section__teacher_assignments__teacher__user=request.user,
            student__section__teacher_assignments__academic_year=F(
                "exam__academic_year"
            ),
        ).distinct()

    # ==========================================
    # SUMMARY
    # ==========================================
    total_students = results.count()

    pass_students = results.filter(
        result="PASS"
    ).count()

    fail_students = results.filter(
        result="FAIL"
    ).count()

    average_percentage = (
        results.aggregate(
            Avg("percentage")
        )["percentage__avg"]
        or 0
    )

    # ==========================================
    # TOPPER
    # ==========================================
    topper = (
        results.select_related(
            "student",
            "grade",
        )
        .order_by("-percentage")
        .first()
    )

    # ==========================================
    # LOWEST
    # ==========================================
    lowest = (
        results.select_related(
            "student",
            "grade",
        )
        .order_by("percentage")
        .first()
    )

    context = {
        "total_students": total_students,
        "pass_students": pass_students,
        "fail_students": fail_students,
        "average_percentage": round(
            average_percentage,
            2,
        ),
        "topper": topper,
        "lowest": lowest,
    }

    return render(
        request,
        "exams/result_analytics.html",
        context,
    )
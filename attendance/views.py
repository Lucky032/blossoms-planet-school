from django.contrib import messages
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Q
from academics.models import (
    SchoolClass,
    Section,
    Student,
    TeacherAssignment,
)

from .models import Attendance

from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_roles


@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def attendance_list(request):

    attendance = (
        Attendance.objects.select_related(
            "student",
            "student__school_class",
            "student__section",
            "student__academic_year",
        )
    )

    # ==========================================
    # TEACHER ACCESS CONTROL
    # ==========================================
    if request.user.userprofile.role == "Teacher":

        attendance = attendance.filter(
            student__school_class__teacher_assignments__teacher__user=request.user,
            student__section__teacher_assignments__teacher__user=request.user,
            student__academic_year__teacher_assignments__teacher__user=request.user,
        ).distinct()

    # Filters
    search = request.GET.get("search", "")
    date = request.GET.get("date", "")
    school_class = request.GET.get("class", "")
    section = request.GET.get("section", "")
    status = request.GET.get("status", "")

    if search:
        attendance = attendance.filter(
            Q(student__admission_number__icontains=search) |
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search)
        )

    if date:
        attendance = attendance.filter(date=date)

    if school_class:
        attendance = attendance.filter(
            student__school_class_id=school_class
        )

    if section:
        attendance = attendance.filter(
            student__section_id=section
        )

    if status:
        attendance = attendance.filter(status=status)

    attendance = attendance.order_by(
        "-date",
        "student__admission_number"
    )

    # Summary Cards
    total = attendance.count()
    present = attendance.filter(status="Present").count()
    absent = attendance.filter(status="Absent").count()
    leave = attendance.filter(status="Leave").count()

    # Pagination
    paginator = Paginator(attendance, 10)
    page_number = request.GET.get("page")
    attendance = paginator.get_page(page_number)

    # ==========================================
    # TEACHER FILTER OPTIONS
    # ==========================================
    if request.user.userprofile.role == "Teacher":

        assignments = TeacherAssignment.objects.filter(
            teacher__user=request.user
        ).select_related(
            "school_class",
            "section",
        )

        teacher_class_ids = assignments.values_list(
            "school_class_id",
            flat=True
        ).distinct()

        teacher_section_ids = assignments.values_list(
            "section_id",
            flat=True
        ).distinct()

        classes = SchoolClass.objects.filter(
            id__in=teacher_class_ids
        ).order_by("display_order")

        sections = Section.objects.filter(
            id__in=teacher_section_ids
        ).order_by(
            "school_class",
            "name"
        )

    else:

        classes = SchoolClass.objects.all().order_by(
            "display_order"
        )

        sections = Section.objects.all().order_by(
            "school_class",
            "name"
        )

    context = {
        "attendance": attendance,
        "classes": classes,
        "sections": sections,
        "search": search,
        "date": date,
        "selected_class": school_class,
        "selected_section": section,
        "status": status,
        "total": total,
        "present": present,
        "absent": absent,
        "leave": leave,
    }

    return render(
        request,
        "attendance/attendance_list.html",
        context,
    )

@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def mark_attendance(request):

    if request.user.userprofile.role == "Teacher":

        teacher_assignments = TeacherAssignment.objects.filter(
            teacher__user=request.user
        ).select_related(
            "school_class",
            "section",
            "academic_year",
        )

        allowed_class_ids = teacher_assignments.values_list(
            "school_class_id",
            flat=True
        ).distinct()

        allowed_section_ids = teacher_assignments.values_list(
            "section_id",
            flat=True
        ).distinct()

        classes = SchoolClass.objects.filter(
            id__in=allowed_class_ids
        ).order_by("display_order")

        sections = Section.objects.filter(
            id__in=allowed_section_ids
        ).order_by(
            "school_class",
            "name"
        )

    else:

        classes = SchoolClass.objects.all().order_by(
            "display_order"
        )

        sections = Section.objects.all().order_by(
            "school_class",
            "name"
        )

    students = Student.objects.none()

    selected_class = request.GET.get("class", "")
    selected_section = request.GET.get("section", "")
    attendance_date = request.GET.get("date", "")

    attendance_map = {}

    # ==========================================
    # GET ACCESS VALIDATION
    # ==========================================
    if (
        request.user.userprofile.role == "Teacher"
        and selected_class
        and selected_section
    ):

        has_assignment = TeacherAssignment.objects.filter(
            teacher__user=request.user,
            school_class_id=selected_class,
            section_id=selected_section,
        ).exists()

        if not has_assignment:
            messages.error(
                request,
                "You are not assigned to this class and section."
            )

            return redirect("mark_attendance")

    # ==========================================
    # LOAD STUDENTS
    # ==========================================
    if selected_class and selected_section:

        students = Student.objects.filter(
            school_class_id=selected_class,
            section_id=selected_section,
            is_active=True,
        ).order_by(
            "admission_number",
        )

        # Teacher gets only assigned students
        if request.user.userprofile.role == "Teacher":

            students = students.filter(
                school_class__teacher_assignments__teacher__user=request.user,
                section__teacher_assignments__teacher__user=request.user,
                academic_year__teacher_assignments__teacher__user=request.user,
            ).distinct()

    # ==========================================
    # EXISTING ATTENDANCE
    # ==========================================
    if students.exists() and attendance_date:

        existing_attendance = Attendance.objects.filter(
            date=attendance_date,
            student__in=students,
        )

        attendance_map = {
            record.student_id: record.status
            for record in existing_attendance
        }

    # ==========================================
    # POST
    # ==========================================
    if request.method == "POST":

        attendance_date = request.POST.get(
            "attendance_date"
        )

        selected_class = request.POST.get(
            "selected_class"
        )

        selected_section = request.POST.get(
            "selected_section"
        )

        # Teacher POST validation
        if request.user.userprofile.role == "Teacher":

            has_assignment = TeacherAssignment.objects.filter(
                teacher__user=request.user,
                school_class_id=selected_class,
                section_id=selected_section,
            ).exists()

            if not has_assignment:

                messages.error(
                    request,
                    "You are not assigned to this class and section."
                )

                return redirect("mark_attendance")

        students = Student.objects.filter(
            school_class_id=selected_class,
            section_id=selected_section,
            is_active=True,
        )

        # Teacher can submit only assigned students
        if request.user.userprofile.role == "Teacher":

            students = students.filter(
                school_class__teacher_assignments__teacher__user=request.user,
                section__teacher_assignments__teacher__user=request.user,
                academic_year__teacher_assignments__teacher__user=request.user,
            ).distinct()

        for student in students:

            status = request.POST.get(
                f"status_{student.id}",
                "Present",
            )

            Attendance.objects.update_or_create(
                student=student,
                date=attendance_date,
                defaults={
                    "status": status,
                    "recorded_by": request.user,
                },
            )

        messages.success(
            request,
            "Attendance saved successfully.",
        )

        return redirect("attendance_list")

    context = {
        "classes": classes,
        "sections": sections,
        "students": students,
        "selected_class": selected_class,
        "selected_section": selected_section,
        "attendance_date": attendance_date,
        "attendance_map": attendance_map,
    }

    return render(
        request,
        "attendance/mark_attendance.html",
        context,
    )



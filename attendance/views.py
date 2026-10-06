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

    # ==========================================
    # BASE ATTENDANCE QUERY
    # ==========================================

    attendance = (
        Attendance.objects.select_related(
            "student",
            "student__school_class",
            "student__section",
            "student__academic_year",
        )
    )

    user_role = request.user.userprofile.role

    # ==========================================
    # TEACHER ACCESS CONTROL
    # ==========================================

    if user_role == "Teacher":

        attendance = attendance.filter(
            student__school_class__teacher_assignments__teacher__user=request.user,
            student__section__teacher_assignments__teacher__user=request.user,
            student__academic_year__teacher_assignments__teacher__user=request.user,
        ).distinct()

    # ==========================================
    # FILTERS
    # ==========================================

    search = request.GET.get("search", "")
    selected_date = request.GET.get("date", "")
    school_class = request.GET.get("class", "")
    section = request.GET.get("section", "")

    # ==========================================
    # SEARCH
    # ==========================================

    if search:

        attendance = attendance.filter(
            Q(student__admission_number__icontains=search)
            | Q(student__first_name__icontains=search)
            | Q(student__last_name__icontains=search)
        )

    # ==========================================
    # DATE FILTER
    # ==========================================

    if selected_date:

        attendance = attendance.filter(
            date=selected_date
        )

    # ==========================================
    # CLASS FILTER
    # ==========================================

    if school_class:

        attendance = attendance.filter(
            student__school_class_id=school_class
        )

    # ==========================================
    # SECTION FILTER
    # ==========================================

    if section:

        attendance = attendance.filter(
            student__section_id=section
        )

    # ==========================================
    # ORDER
    # ==========================================

    attendance = attendance.order_by(
        "-date",
        "student__admission_number",
    )

    # ==========================================
    # SUMMARY
    # ==========================================

    total = attendance.count()

    present = attendance.filter(
        status="Present"
    ).count()

    absent = attendance.filter(
        status="Absent"
    ).count()

    # Attendance percentage
    if total > 0:

        attendance_percentage = round(
            (present / total) * 100,
            2
        )

    else:

        attendance_percentage = 0

    # ==========================================
    # CLASS-WISE SUMMARY
    # ==========================================

    class_summary = []

    if school_class:

        class_records = attendance

        class_total = class_records.count()

        class_present = class_records.filter(
            status="Present"
        ).count()

        class_absent = class_records.filter(
            status="Absent"
        ).count()

        if class_total > 0:

            class_percentage = round(
                (class_present / class_total) * 100,
                2
            )

        else:

            class_percentage = 0

        class_summary = {
            "total": class_total,
            "present": class_present,
            "absent": class_absent,
            "percentage": class_percentage,
        }

    # ==========================================
    # STUDENT-WISE OVERALL SUMMARY
    # ==========================================

    student_summary = {}

    for record in attendance:

        student_id = record.student_id

        if student_id not in student_summary:

            student_summary[student_id] = {
                "student": record.student,
                "present": 0,
                "absent": 0,
                "total": 0,
            }

        student_summary[student_id]["total"] += 1

        if record.status == "Present":

            student_summary[student_id]["present"] += 1

        elif record.status == "Absent":

            student_summary[student_id]["absent"] += 1

    student_summary_list = []

    for item in student_summary.values():

        if item["total"] > 0:

            item["percentage"] = round(
                (item["present"] / item["total"]) * 100,
                2
            )

        else:

            item["percentage"] = 0

        student_summary_list.append(item)

    # ==========================================
    # FILTER OPTIONS
    # ==========================================

    if user_role == "Teacher":

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
        ).order_by(
            "display_order"
        )

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

    # ==========================================
    # PAGINATION
    # ==========================================

    paginator = Paginator(
        attendance,
        10
    )

    page_number = request.GET.get("page")

    attendance_page = paginator.get_page(
        page_number
    )

    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        "attendance": attendance_page,

        # Filters
        "classes": classes,
        "sections": sections,
        "search": search,
        "date": selected_date,
        "selected_class": school_class,
        "selected_section": section,

        # Summary
        "total": total,
        "present": present,
        "absent": absent,
        "attendance_percentage": attendance_percentage,

        # Class summary
        "class_summary": class_summary,

        # Student summary
        "student_summary": student_summary_list,
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



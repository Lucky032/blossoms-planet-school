from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date

from academics.models import (
    Student,
    SchoolClass,
    Subject,
    AcademicYear,
    Section,
    TeacherAssignment,
)

from admissions.models import AdmissionEnquiry
from staff.models import Staff, StaffAttendance
from events.models import Event
from reviews.models import Review


@login_required
def dashboard(request):

    # ==========================
    # Dashboard Cards
    # ==========================

    student_count = Student.objects.count()

    teacher_count = Staff.objects.filter(
        role="Teacher",
        is_active=True
    ).count()

    class_count = SchoolClass.objects.count()

    subject_count = Subject.objects.count()

    academic_year_count = AcademicYear.objects.count()

    section_count = Section.objects.count()

    teacher_assignment_count = TeacherAssignment.objects.count()

    admission_count = AdmissionEnquiry.objects.count()

    event_count = Event.objects.filter(
        is_active=True
    ).count()

    review_count = Review.objects.filter(
        is_active=True
    ).count()


    # ==========================
    # Student Statistics
    # ==========================

    active_students = Student.objects.filter(
        is_active=True
    ).count()

    inactive_students = Student.objects.filter(
        is_active=False
    ).count()

    male_students = Student.objects.filter(
        gender="Male"
    ).count()

    female_students = Student.objects.filter(
        gender="Female"
    ).count()


    # ==========================
    # Today's Staff Attendance
    # ==========================

    today = date.today()

    # Only active staff
    active_staff = Staff.objects.filter(
        is_active=True
    ).order_by("employee_id")

    # Total active staff
    staff_total = active_staff.count()

    # Today's attendance records
    today_attendance = StaffAttendance.objects.filter(
        date=today,
        staff__in=active_staff,
    )

    # Present
    staff_present = today_attendance.filter(
        status="Present"
    ).count()

    # Absent
    staff_absent = today_attendance.filter(
        status="Absent"
    ).count()

    # Paid Leave
    staff_paid_leave = today_attendance.filter(
        status="Leave",
        leave_type="Paid",
    ).count()

    # Unpaid Leave
    staff_unpaid_leave = today_attendance.filter(
        status="Leave",
        leave_type="Unpaid",
    ).count()

    # Total attendance records marked today
    staff_attendance_marked = today_attendance.count()

    # Staff attendance data for dashboard table
    staff_attendance_data = []

    for staff in active_staff:

        attendance = today_attendance.filter(
            staff=staff
        ).first()

        staff_attendance_data.append({
            "staff": staff,
            "attendance": attendance,
        })

    # ==========================
    # Overall Staff Attendance
    # ==========================

    staff_attendance_summary = []

    for staff in active_staff:

        records = StaffAttendance.objects.filter(
            staff=staff
        )

        present_days = records.filter(
            status="Present"
        ).count()

        absent_days = records.filter(
            status="Absent"
        ).count()

        paid_leave_days = records.filter(
            status="Leave",
            leave_type="Paid",
        ).count()

        unpaid_leave_days = records.filter(
            status="Leave",
            leave_type="Unpaid",
        ).count()

        total_marked_days = records.count()

        # Attendance percentage including leave
        if total_marked_days > 0:
            attendance_percentage = round(
                (present_days / total_marked_days) * 100,
                2
            )
        else:
            attendance_percentage = 0

        # Working-day attendance percentage
        working_days = present_days + absent_days

        if working_days > 0:
            working_day_percentage = round(
                (present_days / working_days) * 100,
                2
            )
        else:
            working_day_percentage = 0

        staff_attendance_summary.append({
            "staff": staff,
            "present_days": present_days,
            "absent_days": absent_days,
            "paid_leave_days": paid_leave_days,
            "unpaid_leave_days": unpaid_leave_days,
            "total_marked_days": total_marked_days,
            "attendance_percentage": attendance_percentage,
            "working_day_percentage": working_day_percentage,
        })


    # ==========================
    # Recent Admission Enquiries
    # ==========================

    recent_admissions = AdmissionEnquiry.objects.order_by(
        "-created_at"
    )[:5]


    # ==========================
    # Upcoming Events
    # ==========================

    recent_events = Event.objects.filter(
        is_active=True
    ).order_by(
        "event_date"
    )[:5]


    # ==========================
    # Latest Reviews
    # ==========================

    recent_reviews = Review.objects.filter(
        is_active=True
    ).order_by(
        "display_order"
    )[:5]


    # ==========================
    # Dashboard Context
    # ==========================

    context = {

        # --------------------------
        # Dashboard Cards
        # --------------------------

        "student_count": student_count,
        "teacher_count": teacher_count,
        "class_count": class_count,
        "subject_count": subject_count,
        "academic_year_count": academic_year_count,
        "section_count": section_count,
        "teacher_assignment_count": teacher_assignment_count,
        "admission_count": admission_count,
        "event_count": event_count,
        "review_count": review_count,


        # --------------------------
        # Student Statistics
        # --------------------------

        "active_students": active_students,
        "inactive_students": inactive_students,
        "male_students": male_students,
        "female_students": female_students,


        # --------------------------
        # Today's Staff Attendance
        # --------------------------

        "staff_total": staff_total,
        "staff_present": staff_present,
        "staff_absent": staff_absent,
        "staff_paid_leave": staff_paid_leave,
        "staff_unpaid_leave": staff_unpaid_leave,
        "staff_attendance_marked": staff_attendance_marked,
        "staff_attendance_data": staff_attendance_data,
        "today": today,
        # Overall Staff Attendance
        "staff_attendance_summary": staff_attendance_summary,


        # --------------------------
        # Recent Data
        # --------------------------

        "recent_admissions": recent_admissions,
        "recent_events": recent_events,
        "recent_reviews": recent_reviews,


        # --------------------------
        # Charts
        # --------------------------

        "chart_students": [
            student_count,
            active_students,
            inactive_students,
        ],

        "chart_gender": [
            male_students,
            female_students,
        ],
    }


    # ==========================
    # Render Dashboard
    # ==========================

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )
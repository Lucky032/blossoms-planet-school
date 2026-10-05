from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from academics.models import (
    Student,
    SchoolClass,
    Subject,
    AcademicYear,
    Section,
    TeacherAssignment,
)

from admissions.models import AdmissionEnquiry
from staff.models import Staff
from events.models import Event
from reviews.models import Review

@login_required
def dashboard(request):

    # ==========================
    # Dashboard Cards
    # ==========================

    student_count = Student.objects.count()

    teacher_count = Staff.objects.filter(
        role="Teacher"
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

    context = {

        # Dashboard Cards
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

        # Student Statistics
        "active_students": active_students,
        "inactive_students": inactive_students,
        "male_students": male_students,
        "female_students": female_students,

        # Recent Data
        "recent_admissions": recent_admissions,
        "recent_events": recent_events,
        "recent_reviews": recent_reviews,

        # Charts
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

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )
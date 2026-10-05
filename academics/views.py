from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, SchoolClass, Section, AcademicYear, Section, Subject, TeacherAssignment
from django.db.models import Q

from django.core.paginator import Paginator
from django.contrib import messages

from .forms import StudentForm, SchoolClassForm, AcademicYearForm, SectionForm, SubjectForm, TeacherAssignmentForm

from django.contrib.auth.decorators import login_required
from accounts.decorators import allowed_roles





@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def student_list(request):

    query = request.GET.get("q")
    class_id = request.GET.get("class") or None
    section_id = request.GET.get("section") or None

    if class_id == "None":
        class_id = None

    if section_id == "None":
        section_id = None

    students = Student.objects.select_related(
        "school_class",
        "section",
        "academic_year"
    ).all()

    # ==========================================
    # TEACHER ACCESS CONTROL
    # ==========================================
    if request.user.userprofile.role == "Teacher":

        students = students.filter(
            school_class__teacher_assignments__teacher__user=request.user,
            section__teacher_assignments__teacher__user=request.user,
            academic_year__teacher_assignments__teacher__user=request.user,
        ).distinct()

    # ==========================================
    # SEARCH
    # ==========================================
    if query:
        students = students.filter(
            Q(admission_number__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(father_name__icontains=query)
        )

    # ==========================================
    # CLASS FILTER
    # ==========================================
    if class_id:
        students = students.filter(
            school_class_id=class_id
        )

    # ==========================================
    # SECTION FILTER
    # ==========================================
    if section_id:
        students = students.filter(
            section_id=section_id
        )

    # Show sections only for selected class
    if class_id:
        sections = Section.objects.filter(
            school_class_id=class_id
        ).order_by("name")
    else:
        sections = Section.objects.all().order_by(
            "school_class",
            "name"
        )

    classes = SchoolClass.objects.all().order_by(
        "display_order"
    )

    paginator = Paginator(students, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "students": page_obj,
        "page_obj": page_obj,
        "query": query,
        "classes": classes,
        "sections": sections,
        "selected_class": class_id,
        "selected_section": section_id,
    }

    return render(
        request,
        "academics/student_list.html",
        context,
    )

@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES  )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student added successfully!"
            
            )

            return redirect("student_list")

    else:

        form = StudentForm()

    return render(
        request,
        "academics/add_student.html",
        {
            "form": form
        }
    )

@login_required
@allowed_roles("Admin", "Principal", "Teacher")
def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    # ==========================================
    # TEACHER ACCESS CONTROL
    # ==========================================
    if request.user.userprofile.role == "Teacher":

        has_assignment = TeacherAssignment.objects.filter(
            teacher__user=request.user,
            school_class=student.school_class,
            section=student.section,
            academic_year=student.academic_year,
        ).exists()

        if not has_assignment:
            messages.error(
                request,
                "You do not have permission to view this student."
            )
            return redirect("student_list")

    context = {
        "student": student
    }

    return render(
        request,
        "academics/student_detail.html",
        context,
    )

@login_required
@allowed_roles("Admin", "Principal")
def edit_student(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Student updated successfully!"
            )

            return redirect("student_list")

    else:

        form = StudentForm(
            instance=student
        )

    return render(

        request,

        "academics/edit_student.html",

        {

            "form": form,
            "student": student

        }

    )

@login_required
@allowed_roles("Admin", "Principal")
def delete_student(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        student.delete()

        messages.success(
            request,
            "Student deleted successfully!"
        )

        return redirect("student_list")
    
    return render(

        request,

        "academics/delete_student.html",

        {

            "student": student

        }

    )


@login_required
@allowed_roles("Admin", "Principal")
def class_list(request):

    classes = SchoolClass.objects.all()

    return render(
        request,
        "academics/class_list.html",
        {
            "classes": classes
        }
    )

@login_required
@allowed_roles("Admin", "Principal")
def class_create(request):

    if request.method == "POST":

        form = SchoolClassForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Class added successfully."
            )

            return redirect("class_list")

    else:

        form = SchoolClassForm()

    return render(
        request,
        "academics/class_form.html",
        {
            "form": form,
            "title": "Add Class",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def class_update(request, pk):

    school_class = get_object_or_404(
        SchoolClass,
        pk=pk
    )

    if request.method == "POST":

        form = SchoolClassForm(
            request.POST,
            instance=school_class,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Class updated successfully."
            )

            return redirect("class_list")

    else:

        form = SchoolClassForm(
            instance=school_class
        )

    return render(
        request,
        "academics/class_form.html",
        {
            "form": form,
            "title": "Edit Class",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def class_delete(request, pk):

    school_class = get_object_or_404(
        SchoolClass,
        pk=pk
    )

    if request.method == "POST":

        school_class.delete()

        messages.success(
            request,
            "Class deleted successfully."
        )

        return redirect("class_list")

    return render(
        request,
        "academics/class_delete.html",
        {
            "school_class": school_class,
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def academic_year_list(request):

    academic_years = AcademicYear.objects.all()

    return render(
        request,
        "academics/academic_year_list.html",
        {
            "academic_years": academic_years,
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def academic_year_create(request):

    if request.method == "POST":

        form = AcademicYearForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Academic year added successfully.",
            )

            return redirect("academic_year_list")

    else:

        form = AcademicYearForm()

    return render(
        request,
        "academics/academic_year_form.html",
        {
            "form": form,
            "title": "Add Academic Year",
        },
    )

@login_required
@allowed_roles("Admin", "Principal")
def academic_year_update(request, pk):

    academic_year = get_object_or_404(
        AcademicYear,
        pk=pk,
    )

    if request.method == "POST":

        form = AcademicYearForm(
            request.POST,
            instance=academic_year,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Academic year updated successfully.",
            )

            return redirect("academic_year_list")

    else:

        form = AcademicYearForm(
            instance=academic_year,
        )

    return render(
        request,
        "academics/academic_year_form.html",
        {
            "form": form,
            "title": "Edit Academic Year",
        },
    )

@login_required
@allowed_roles("Admin", "Principal")
def academic_year_delete(request, pk):

    academic_year = get_object_or_404(
        AcademicYear,
        pk=pk,
    )

    if request.method == "POST":

        academic_year.delete()

        messages.success(
            request,
            "Academic year deleted successfully.",
        )

        return redirect("academic_year_list")

    return render(
        request,
        "academics/academic_year_delete.html",
        {
            "academic_year": academic_year,
        },
    )

# =========================
# SECTION MANAGEMENT
# =========================


@login_required
@allowed_roles("Admin", "Principal")
def section_list(request):
    sections = Section.objects.select_related("school_class").all()

    return render(
        request,
        "academics/section_list.html",
        {"sections": sections}
    )

@login_required
@allowed_roles("Admin", "Principal")
def section_create(request):
    if request.method == "POST":
        form = SectionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Section added successfully.")
            return redirect("section_list")

    else:
        form = SectionForm()

    return render(
        request,
        "academics/section_form.html",
        {
            "form": form,
            "title": "Add Section"
        }
    )

@login_required
@allowed_roles("Admin", "Principal")
def section_update(request, pk):
    section = get_object_or_404(Section, pk=pk)

    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)

        if form.is_valid():
            form.save()
            messages.success(request, "Section updated successfully.")
            return redirect("section_list")

    else:
        form = SectionForm(instance=section)

    return render(
        request,
        "academics/section_form.html",
        {
            "form": form,
            "title": "Edit Section"
        }
    )


@login_required
@allowed_roles("Admin", "Principal")
def section_delete(request, pk):
    section = get_object_or_404(Section, pk=pk)

    if request.method == "POST":
        section.delete()
        messages.success(request, "Section deleted successfully.")
        return redirect("section_list")

    return render(
        request,
        "academics/section_delete.html",
        {"section": section}
    )

# =========================
# SUBJECT MANAGEMENT
# =========================

@login_required
@allowed_roles("Admin", "Principal")
def subject_list(request):
    subjects = Subject.objects.all()

    return render(
        request,
        "academics/subject_list.html",
        {"subjects": subjects}
    )


@login_required
@allowed_roles("Admin", "Principal")
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Subject added successfully.")
            return redirect("subject_list")

    else:
        form = SubjectForm()

    return render(
        request,
        "academics/subject_form.html",
        {
            "form": form,
            "title": "Add Subject"
        }
    )


@login_required
@allowed_roles("Admin", "Principal")
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)

        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect("subject_list")

    else:
        form = SubjectForm(instance=subject)

    return render(
        request,
        "academics/subject_form.html",
        {
            "form": form,
            "title": "Edit Subject"
        }
    )


@login_required
@allowed_roles("Admin", "Principal")
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == "POST":
        subject.delete()
        messages.success(request, "Subject deleted successfully.")
        return redirect("subject_list")

    return render(
        request,
        "academics/subject_delete.html",
        {"subject": subject}
    )

# =========================
# TEACHER ASSIGNMENT MANAGEMENT
# =========================


@login_required
@allowed_roles("Admin", "Principal")
def teacher_assignment_list(request):
    assignments = TeacherAssignment.objects.select_related(
        "teacher",
        "subject",
        "school_class",
        "section",
        "academic_year",
    ).all()

    return render(
        request,
        "academics/teacher_assignment_list.html",
        {"assignments": assignments}
    )

@login_required
@allowed_roles("Admin", "Principal")
def teacher_assignment_create(request):
    if request.method == "POST":
        form = TeacherAssignmentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Teacher assignment added successfully."
            )
            return redirect("teacher_assignment_list")

    else:
        form = TeacherAssignmentForm()

    return render(
        request,
        "academics/teacher_assignment_form.html",
        {
            "form": form,
            "title": "Add Teacher Assignment"
        }
    )

@login_required
@allowed_roles("Admin", "Principal")
def teacher_assignment_update(request, pk):
    assignment = get_object_or_404(
        TeacherAssignment,
        pk=pk
    )

    if request.method == "POST":
        form = TeacherAssignmentForm(
            request.POST,
            instance=assignment
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Teacher assignment updated successfully."
            )
            return redirect("teacher_assignment_list")

    else:
        form = TeacherAssignmentForm(
            instance=assignment
        )

    return render(
        request,
        "academics/teacher_assignment_form.html",
        {
            "form": form,
            "title": "Edit Teacher Assignment"
        }
    )

@login_required
@allowed_roles("Admin", "Principal")
def teacher_assignment_delete(request, pk):
    assignment = get_object_or_404(
        TeacherAssignment,
        pk=pk
    )

    if request.method == "POST":
        assignment.delete()
        messages.success(
            request,
            "Teacher assignment deleted successfully."
        )
        return redirect("teacher_assignment_list")

    return render(
        request,
        "academics/teacher_assignment_delete.html",
        {"assignment": assignment}
    )
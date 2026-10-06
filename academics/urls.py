from django.urls import path
from . import views

urlpatterns = [

    path(
    "",
    views.academics_home,
    name="academics_home",
    ),

    path(
        "students/",
        views.student_list,
        name="student_list",
    ),

    path(
        "students/add/",
        views.add_student,
        name="add_student",
    ),

    path(
        "students/<int:pk>/",
        views.student_detail,
        name="student_detail",
    ),

    path(
        "students/<int:pk>/edit/",
        views.edit_student,
        name="edit_student",
    ),

    path(
        "students/<int:pk>/delete/",
        views.delete_student,
        name="delete_student",
    ),
    path("classes/", views.class_list, name="class_list"),
    path("classes/add/", views.class_create, name="class_create"),
    path("classes/<int:pk>/edit/", views.class_update, name="class_update"),
    path("classes/<int:pk>/delete/", views.class_delete, name="class_delete"),
    path(
    "academic-years/",
    views.academic_year_list,
    name="academic_year_list",
),

path(
    "academic-years/add/",
    views.academic_year_create,
    name="academic_year_create",
),

path(
    "academic-years/<int:pk>/edit/",
    views.academic_year_update,
    name="academic_year_update",
),

path(
    "academic-years/<int:pk>/delete/",
    views.academic_year_delete,
    name="academic_year_delete",
),

path("sections/", views.section_list, name="section_list"),
path("sections/add/", views.section_create, name="section_create"),
path("sections/<int:pk>/edit/", views.section_update, name="section_update"),
path("sections/<int:pk>/delete/", views.section_delete, name="section_delete"),

# Subjects
path("subjects/", views.subject_list, name="subject_list"),
path("subjects/add/", views.subject_create, name="subject_create"),
path("subjects/<int:pk>/edit/", views.subject_update, name="subject_update"),
path("subjects/<int:pk>/delete/", views.subject_delete, name="subject_delete"),

# Teacher Assignments
path(
    "teacher-assignments/",
    views.teacher_assignment_list,
    name="teacher_assignment_list",
),
path(
    "teacher-assignments/add/",
    views.teacher_assignment_create,
    name="teacher_assignment_create",
),
path(
    "teacher-assignments/<int:pk>/edit/",
    views.teacher_assignment_update,
    name="teacher_assignment_update",
),
path(
    "teacher-assignments/<int:pk>/delete/",
    views.teacher_assignment_delete,
    name="teacher_assignment_delete",
),


]
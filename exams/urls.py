from django.urls import path
from . import views

urlpatterns = [
    # Exam CRUD
    path("", views.exam_list, name="exam_list"),
    path("add/", views.exam_create, name="exam_create"),
    path("<int:pk>/edit/", views.exam_update, name="exam_update"),
    path("<int:pk>/delete/", views.exam_delete, name="exam_delete"),
    path("grades/", views.grade_list, name="grade_list"),
    path("grades/add/", views.grade_create, name="grade_create"),
    path("grades/<int:pk>/edit/", views.grade_update, name="grade_update"),
    path("grades/<int:pk>/delete/", views.grade_delete, name="grade_delete"),
    # Exam Subject Management
    path("subjects/", views.exam_subject_list, name="exam_subject_list"),
    path("subjects/add/", views.exam_subject_create, name="exam_subject_create"),
    path("subjects/<int:pk>/edit/", views.exam_subject_update, name="exam_subject_update"),
    path("subjects/<int:pk>/delete/", views.exam_subject_delete, name="exam_subject_delete"),
    path("marks-entry/", views.marks_entry, name="marks_entry"),
    path("student-marks/", views.student_mark_list, name="student_mark_list"),
    path("student-marks/<int:pk>/edit/", views.student_mark_update, name="student_mark_update"),
    path("student-marks/<int:pk>/delete/", views.student_mark_delete, name="student_mark_delete"),
    path("rankings/", views.class_ranking_list, name="class_ranking_list"),
    path("analytics/", views.result_analytics, name="result_analytics"),
]
from django.urls import path

from . import views


urlpatterns = [

    path(
    "attendance/",
    views.staff_attendance,
    name="staff_attendance",
    ),

    path(
        "",
        views.staff_list,
        name="staff_list",
    ),

    path(
        "add/",
        views.staff_create,
        name="staff_create",
    ),

    path(
        "<int:pk>/",
        views.staff_detail,
        name="staff_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.staff_update,
        name="staff_update",
    ),

    path(
        "<int:pk>/delete/",
        views.staff_delete,
        name="staff_delete",
    ),

]
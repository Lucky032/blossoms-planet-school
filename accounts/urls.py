from django.urls import path

from . import views

urlpatterns = [

    # Authentication
    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    path(
        "signup/",
        views.signup_view,
        name="signup",
    ),

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password",
    ),

    path(
        "verify-otp/",
        views.verify_otp,
        name="verify_otp",
    ),

    path(
        "reset-password/",
        views.reset_password,
        name="reset_password",
    ),

    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    # User Management
    path(
        "users/",
        views.user_list,
        name="user_list",
    ),

    path(
        "users/add/",
        views.user_create,
        name="user_create",
    ),

    path(
        "users/<int:pk>/edit/",
        views.user_update,
        name="user_update",
    ),

    path(
        "users/<int:pk>/delete/",
        views.user_delete,
        name="user_delete",
    ),

    path("pending-teachers/", views.pending_teachers, name="pending_teachers"),
    path("approve-teacher/<int:user_id>/", views.approve_teacher, name="approve_teacher"),
    path("reject-teacher/<int:user_id>/", views.reject_teacher, name="reject_teacher"),
]
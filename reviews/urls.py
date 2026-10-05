from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.review_list,
        name="review_list",
    ),

    path(
        "create/",
        views.review_create,
        name="review_create",
    ),

    path(
        "<int:pk>/edit/",
        views.review_update,
        name="review_update",
    ),

    path(
        "<int:pk>/delete/",
        views.review_delete,
        name="review_delete",
    ),
]
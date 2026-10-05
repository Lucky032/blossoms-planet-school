from django.urls import path
from . import views


urlpatterns = [

    # ==========================
    # Fee Structure
    # ==========================


    path(
        "paytm/checkout/<int:student_id>/<int:fee_structure_id>/",
        views.paytm_checkout,
        name="paytm_checkout",
    ),

    path(
        "structure/",
        views.fee_structure_list,
        name="fee_structure_list",
    ),

    path(
        "structure/add/",
        views.fee_structure_create,
        name="fee_structure_create",
    ),

    path(
        "structure/<int:pk>/edit/",
        views.fee_structure_update,
        name="fee_structure_update",
    ),

    path(
        "structure/<int:pk>/delete/",
        views.fee_structure_delete,
        name="fee_structure_delete",
    ),

    # ==========================
    # Fee Collection
    # ==========================

    path(
        "",
        views.fee_collection_list,
        name="fee_collection_list",
    ),

    path(
        "collect/",
        views.fee_collection_create,
        name="fee_collection_create",
    ),

    path(
        "<int:pk>/edit/",
        views.fee_collection_update,
        name="fee_collection_update",
    ),

    path(
        "<int:pk>/delete/",
        views.fee_collection_delete,
        name="fee_collection_delete",
    ),

    # ==========================
    # Paytm Online Payment
    # ==========================

    path(
        "paytm/create/",
        views.paytm_payment_create,
        name="paytm_payment_create",
    ),

    path(
        "paytm/callback/",
        views.fee_payment_callback,
        name="fee_payment_callback",
    ),

    path(
        "paytm/status/<str:order_id>/",
        views.paytm_payment_status,
        name="paytm_payment_status",
    ),
]
from django.urls import path

from . import views

urlpatterns = [

    path(
        "",
        views.admission_enquiry,
        name="admission",
    ),

]
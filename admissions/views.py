from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import AdmissionEnquiryForm


def admission_enquiry(request):

    if request.method == "POST":

        form = AdmissionEnquiryForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your admission enquiry has been submitted successfully."
            )

            return redirect("admission")

    else:

        form = AdmissionEnquiryForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "admissions/admission.html",
        context,
    )
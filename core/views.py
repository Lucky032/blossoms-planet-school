from django.shortcuts import render

from .models import SchoolProfile, Facility, Statistic
from events.models import GalleryImage
from reviews.models import Review


def home(request):

    school = SchoolProfile.objects.first()

    facilities = Facility.objects.filter(
        is_active=True
    )

    gallery = GalleryImage.objects.filter(
        is_active=True
    )[:6]

    reviews = Review.objects.filter(
        is_active=True
    ).order_by("display_order")[:3]

    statistics = Statistic.objects.filter(
        is_active=True
    )

    context = {
        "school": school,
        "facilities": facilities,
        "gallery": gallery,
        "reviews": reviews,
        "statistics": statistics,
    }

    return render(
        request,
        "core/home.html",
        context
    )


def about(request):

    school = SchoolProfile.objects.first()

    context = {
        "school": school,
    }

    return render(
        request,
        "core/about.html",
        context
    )


def contact(request):

    school = SchoolProfile.objects.first()

    context = {
        "school": school,
    }

    return render(
        request,
        "core/contact.html",
        context
    )

def campus_life(request):
    return render(request, "core/campus_life.html")
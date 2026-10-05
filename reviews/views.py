from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ReviewForm
from .models import Review


def review_list(request):

    search = request.GET.get("search", "")

    reviews = Review.objects.all()

    if search:
        reviews = reviews.filter(
            Q(name__icontains=search) |
            Q(designation__icontains=search)
        )

    paginator = Paginator(reviews, 10)

    page = request.GET.get("page")

    return render(
        request,
        "reviews/review_list.html",
        {
            "reviews": paginator.get_page(page),
            "search": search,
        },
    )


def review_create(request):

    if request.method == "POST":

        form = ReviewForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Review created successfully."
            )

            return redirect("review_list")

    else:

        form = ReviewForm()

    return render(
        request,
        "reviews/review_form.html",
        {
            "form": form,
            "title": "Add Review",
        },
    )


def review_update(request, pk):

    review = get_object_or_404(
        Review,
        pk=pk,
    )

    if request.method == "POST":

        form = ReviewForm(
            request.POST,
            request.FILES,
            instance=review,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Review updated successfully."
            )

            return redirect("review_list")

    else:

        form = ReviewForm(
            instance=review,
        )

    return render(
        request,
        "reviews/review_form.html",
        {
            "form": form,
            "title": "Edit Review",
        },
    )


def review_delete(request, pk):

    review = get_object_or_404(
        Review,
        pk=pk,
    )

    if request.method == "POST":

        review.delete()

        messages.success(
            request,
            "Review deleted successfully."
        )

        return redirect("review_list")

    return render(
        request,
        "reviews/review_delete.html",
        {
            "review": review,
        },
    )
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventForm
from .models import Event

from accounts.decorators import allowed_roles
from django.contrib.auth.decorators import login_required


@login_required
@allowed_roles("Admin", "Principal")
def event_list(request):

    search = request.GET.get("search", "")

    events = Event.objects.all()

    if search:
        events = events.filter(
            Q(title__icontains=search)
            | Q(venue__icontains=search)
        )

    paginator = Paginator(events, 10)

    page = request.GET.get("page")

    return render(
        request,
        "events/event_list.html",
        {
            "events": paginator.get_page(page),
            "search": search,
        },
    )

@login_required
@allowed_roles("Admin", "Principal")
def event_create(request):

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event created successfully.",
            )

            return redirect("event_list")

    else:

        form = EventForm()

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "title": "Add Event",
        },
    )

@login_required
@allowed_roles("Admin", "Principal")
def event_update(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk,
    )

    if request.method == "POST":

        form = EventForm(
            request.POST,
            request.FILES,
            instance=event,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event updated successfully.",
            )

            return redirect("event_list")

    else:

        form = EventForm(
            instance=event,
        )

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "title": "Edit Event",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def event_delete(request, pk):

    event = get_object_or_404(
        Event,
        pk=pk,
    )

    if request.method == "POST":

        event.delete()

        messages.success(
            request,
            "Event deleted successfully.",
        )

        return redirect("event_list")

    return render(
        request,
        "events/event_delete.html",
        {
            "event": event,
        },
    )
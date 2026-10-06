from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StaffForm
from .models import Staff, StaffAttendance
from accounts.decorators import allowed_roles
from django.contrib.auth.decorators import login_required


@login_required
@allowed_roles("Admin", "Principal")
def staff_list(request):

    staff = Staff.objects.all()

    search = request.GET.get("search", "")
    role = request.GET.get("role", "")
    status = request.GET.get("status", "")

    if search:
        staff = staff.filter(
            Q(employee_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search)
        )

    if role:
        staff = staff.filter(role=role)

    if status == "active":
        staff = staff.filter(is_active=True)

    elif status == "inactive":
        staff = staff.filter(is_active=False)

    staff = staff.order_by("employee_id")

    paginator = Paginator(staff, 10)
    page_number = request.GET.get("page")
    staff = paginator.get_page(page_number)

    context = {
        "page_obj": staff,
        "staff": staff,
        "search": search,
        "selected_role": role,
        "selected_status": status,
        "roles": Staff.ROLE_CHOICES,

    }

    return render(
        request,
        "staff/staff_list.html",
        context,
    )



@login_required
@allowed_roles("Admin", "Principal")
def staff_create(request):

    if request.method == "POST":

        form = StaffForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Staff added successfully.",
            )

            return redirect("staff_list")

    else:

        form = StaffForm()

    context = {
        "form": form,
        "title": "Add Staff",
    }

    return render(
        request,
        "staff/staff_form.html",
        context,
    )

@login_required
@allowed_roles("Admin", "Principal")
def staff_update(request, pk):

    staff = get_object_or_404(
        Staff,
        pk=pk,
    )

    if request.method == "POST":

        form = StaffForm(
            request.POST,
            request.FILES,
            instance=staff,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Staff updated successfully.",
            )

            return redirect("staff_list")

    else:

        form = StaffForm(
            instance=staff,
        )

    context = {
        "form": form,
        "title": "Edit Staff",
    }

    return render(
        request,
        "staff/staff_form.html",
        context,
    )


@login_required
@allowed_roles("Admin", "Principal")
def staff_detail(request, pk):

    staff = get_object_or_404(
        Staff,
        pk=pk,
    )

    context = {
        "staff": staff,
    }

    return render(
        request,
        "staff/staff_detail.html",
        context,
    )


@login_required
@allowed_roles("Admin", "Principal")
def staff_delete(request, pk):

    staff = get_object_or_404(
        Staff,
        pk=pk,
    )

    if request.method == "POST":

        staff.delete()

        messages.success(
            request,
            "Staff deleted successfully.",
        )

        return redirect("staff_list")

    context = {
        "staff": staff,
    }

    return render(
        request,
        "staff/staff_confirm_delete.html",
        context,
    )

@login_required
@allowed_roles("Admin", "Principal")
def staff_attendance(request):

    selected_date = request.GET.get("date", "")

    if not selected_date:
        from datetime import date
        selected_date = date.today().isoformat()

    staff_members = Staff.objects.filter(
        is_active=True
    ).order_by("employee_id")

    attendance_records = StaffAttendance.objects.filter(
        date=selected_date,
        staff__in=staff_members,
    )

    attendance_data = []

    for staff in staff_members:

        record = attendance_records.filter(
            staff=staff
        ).first()

        attendance_data.append({
            "staff": staff,
            "record": record,
        })

    if request.method == "POST":

        attendance_date = request.POST.get("attendance_date")

        for staff in staff_members:

            status = request.POST.get(
                f"status_{staff.id}",
                "Present",
            )

            leave_type = request.POST.get(
                f"leave_type_{staff.id}",
                "",
            )

            remarks = request.POST.get(
                f"remarks_{staff.id}",
                "",
            )

            if status != "Leave":
                leave_type = ""

            StaffAttendance.objects.update_or_create(
                staff=staff,
                date=attendance_date,
                defaults={
                    "status": status,
                    "leave_type": leave_type or None,
                    "remarks": remarks,
                    "recorded_by": request.user,
                },
            )

        messages.success(
            request,
            "Staff attendance saved successfully.",
        )

        return redirect(
            f"/staff/attendance/?date={attendance_date}"
        )

    context = {
        "attendance_data": attendance_data,
        "selected_date": selected_date,
    }

    return render(
        request,
        "staff/staff_attendance.html",
        context,
    )
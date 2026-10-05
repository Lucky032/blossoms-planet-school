from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    SignupForm,
    LoginForm,
    UserForm,
    UserProfileForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    OTPVerificationForm,
)

from .models import UserProfile, PasswordResetOTP

import random

from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

from staff.models import Staff


# ============================================================
# FORGOT PASSWORD
# ============================================================

def forgot_password(request):

    if request.method == "POST":

        form = ForgotPasswordForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"]

            try:

                user = User.objects.get(email=email)

            except User.DoesNotExist:

                messages.error(
                    request,
                    "No account found with this email.",
                )

                return redirect("forgot_password")

            PasswordResetOTP.objects.filter(
                user=user,
                is_used=False,
            ).delete()

            otp = str(random.randint(100000, 999999))

            PasswordResetOTP.objects.create(
                user=user,
                otp=otp,
            )

            send_mail(
                subject="Password Reset OTP",
                message=f"""
Hello {user.first_name or user.username},

Your OTP is:

{otp}

This OTP is valid for 10 minutes.

Do not share this OTP with anyone.

Blossoms Planet School ERP
""",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )

            request.session["reset_email"] = email

            messages.success(
                request,
                "OTP has been sent to your email.",
            )

            return redirect("verify_otp")

    else:

        form = ForgotPasswordForm()

    return render(
        request,
        "accounts/forgot_password.html",
        {
            "form": form,
        },
    )


# ============================================================
# SIGNUP
# ============================================================

def signup_view(request):

    if request.user.is_authenticated:

        return redirect("dashboard")

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            # ------------------------------------------------
            # Get selected role from signup form
            # ------------------------------------------------

            selected_role = form.cleaned_data["role"]

            # ------------------------------------------------
            # Create User
            # ------------------------------------------------

            user = form.save()

            # ------------------------------------------------
            # First registered account remains Admin
            # ------------------------------------------------

            if User.objects.count() == 1:

                role = "Admin"
                is_approved = True

            else:

                role = selected_role
                is_approved = False

            # ------------------------------------------------
            # Create UserProfile
            # ------------------------------------------------

            UserProfile.objects.create(
                user=user,
                role=role,
                phone=form.cleaned_data["mobile"],
                is_approved=is_approved,
            )

            # ------------------------------------------------
            # Messages
            # ------------------------------------------------

            if role == "Admin":

                messages.success(
                    request,
                    "Admin account created successfully. Please login.",
                )

            elif role == "Teacher":

                messages.success(
                    request,
                    "Teacher registration successful. Your account is waiting for administrator approval.",
                )

            elif role == "Principal":

                messages.success(
                    request,
                    "Principal registration successful. Your account is waiting for administrator approval.",
                )

            return redirect("login")

    else:

        form = SignupForm()

    return render(
        request,
        "accounts/signup.html",
        {
            "form": form,
        },
    )


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:

        return redirect("dashboard")

    form = LoginForm(
        request,
        data=request.POST or None,
    )

    if request.method == "POST":

        if form.is_valid():

            user = form.get_user()

            # ------------------------------------------------
            # Get selected role from login form
            # ------------------------------------------------

            selected_role = form.cleaned_data["role"]

            # ------------------------------------------------
            # Get actual UserProfile
            # ------------------------------------------------

            try:

                profile = UserProfile.objects.get(
                    user=user
                )

            except UserProfile.DoesNotExist:

                messages.error(
                    request,
                    "User profile not found.",
                )

                return redirect("login")

            # ------------------------------------------------
            # Role verification
            # ------------------------------------------------

            if profile.role != selected_role:

                messages.error(
                    request,
                    f"This account is registered as {profile.role}. "
                    f"Please select {profile.role} to login.",
                )

                return redirect("login")

            # ------------------------------------------------
            # Approval verification
            # ------------------------------------------------

            if not profile.is_approved:

                messages.warning(
                    request,
                    "Your account is waiting for administrator approval.",
                )

                return redirect("login")

            # ------------------------------------------------
            # Login
            # ------------------------------------------------

            login(request, user)

            # ------------------------------------------------
            # Remember Me
            # ------------------------------------------------

            if not request.POST.get("remember_me"):

                request.session.set_expiry(0)

            messages.success(
                request,
                "Login successful.",
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid username or password.",
            )

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully.",
    )

    return redirect("login")


# ============================================================
# PROFILE
# ============================================================

@login_required
def profile(request):

    profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
        },
    )


# ============================================================
# USER LIST
# ============================================================

@login_required
def user_list(request):

    users = User.objects.all().order_by("username")

    return render(
        request,
        "accounts/user_list.html",
        {
            "users": users,
        },
    )


# ============================================================
# CREATE USER
# ============================================================

@login_required
def user_create(request):

    if request.method == "POST":

        user_form = UserForm(request.POST)

        profile_form = UserProfileForm(
            request.POST,
            request.FILES,
        )

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)

            user.set_password(
                user_form.cleaned_data["password"]
            )

            user.save()

            profile = profile_form.save(
                commit=False
            )

            profile.user = user

            profile.save()

            messages.success(
                request,
                "User created successfully.",
            )

            return redirect("user_list")

    else:

        user_form = UserForm()

        profile_form = UserProfileForm()

    return render(
        request,
        "accounts/user_form.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


# ============================================================
# UPDATE USER
# ============================================================

@login_required
def user_update(request, pk):

    user = get_object_or_404(
        User,
        pk=pk,
    )

    profile, created = UserProfile.objects.get_or_create(
        user=user
    )

    if request.method == "POST":

        user_form = UserForm(
            request.POST,
            instance=user,
        )

        profile_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if user_form.is_valid() and profile_form.is_valid():

            updated_user = user_form.save(
                commit=False
            )

            password = user_form.cleaned_data.get(
                "password"
            )

            if password:

                updated_user.set_password(
                    password
                )

            updated_user.save()

            profile_form.save()

            messages.success(
                request,
                "User updated successfully.",
            )

            return redirect("user_list")

    else:

        user_form = UserForm(
            instance=user
        )

        user_form.fields["password"].initial = ""

        profile_form = UserProfileForm(
            instance=profile
        )

    return render(
        request,
        "accounts/user_form.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "is_edit": True,
        },
    )


# ============================================================
# DELETE USER
# ============================================================

@login_required
def user_delete(request, pk):

    user = get_object_or_404(
        User,
        pk=pk,
    )

    if request.method == "POST":

        user.delete()

        messages.success(
            request,
            "User deleted successfully.",
        )

        return redirect("user_list")

    return render(
        request,
        "accounts/user_confirm_delete.html",
        {
            "user_obj": user,
        },
    )


# ============================================================
# VERIFY OTP
# ============================================================

def verify_otp(request):

    email = request.session.get("reset_email")

    if not email:

        messages.error(
            request,
            "Please request a new OTP.",
        )

        return redirect("forgot_password")

    try:

        user = User.objects.get(
            email=email
        )

    except User.DoesNotExist:

        messages.error(
            request,
            "User not found.",
        )

        return redirect("forgot_password")

    if request.method == "POST":

        form = OTPVerificationForm(
            request.POST
        )

        if form.is_valid():

            otp = form.cleaned_data["otp"]

            try:

                otp_record = PasswordResetOTP.objects.get(
                    user=user,
                    otp=otp,
                    is_used=False,
                )

            except PasswordResetOTP.DoesNotExist:

                messages.error(
                    request,
                    "Invalid OTP.",
                )

                return redirect("verify_otp")

            if otp_record.is_expired():

                messages.error(
                    request,
                    "OTP has expired.",
                )

                return redirect("forgot_password")

            otp_record.is_used = True

            otp_record.save()

            request.session["otp_verified"] = True

            messages.success(
                request,
                "OTP verified successfully.",
            )

            return redirect("reset_password")

    else:

        form = OTPVerificationForm()

    return render(
        request,
        "accounts/verify_otp.html",
        {
            "form": form,
        },
    )


# ============================================================
# RESET PASSWORD
# ============================================================

def reset_password(request):

    email = request.session.get("reset_email")

    if not request.session.get("otp_verified"):

        messages.error(
            request,
            "Please verify your OTP first.",
        )

        return redirect("verify_otp")

    user = User.objects.get(
        email=email
    )

    if request.method == "POST":

        form = ResetPasswordForm(
            request.POST
        )

        if form.is_valid():

            password = form.cleaned_data[
                "password1"
            ]

            user.set_password(password)

            user.save()

            request.session.pop(
                "reset_email",
                None,
            )

            request.session.pop(
                "otp_verified",
                None,
            )

            messages.success(
                request,
                "Password changed successfully. Please login.",
            )

            return redirect("login")

    else:

        form = ResetPasswordForm()

    return render(
        request,
        "accounts/reset_password.html",
        {
            "form": form,
        },
    )


# ============================================================
# PENDING TEACHERS
# ============================================================

@staff_member_required
def pending_teachers(request):

    teachers = UserProfile.objects.filter(
        role="Teacher",
        is_approved=False,
    ).select_related("user")

    return render(
        request,
        "accounts/pending_teachers.html",
        {
            "teachers": teachers,
        },
    )


# ============================================================
# APPROVE TEACHER
# ============================================================

@staff_member_required
def approve_teacher(request, user_id):

    teacher = get_object_or_404(
        UserProfile,
        user_id=user_id,
    )

    if request.method == "POST":

        gender = request.POST.get("gender")

        qualification = request.POST.get(
            "qualification"
        )

        experience = request.POST.get(
            "experience"
        )

        salary = request.POST.get(
            "salary"
        )

        joining_date = request.POST.get(
            "joining_date"
        )

        address = request.POST.get(
            "address"
        )

        # ------------------------------------------------
        # Prevent duplicate staff records
        # ------------------------------------------------

        if Staff.objects.filter(
            email=teacher.user.email
        ).exists():

            messages.error(
                request,
                "Staff already exists.",
            )

            return redirect(
                "pending_teachers"
            )

        # ------------------------------------------------
        # Generate Employee ID
        # ------------------------------------------------

        last_staff = Staff.objects.order_by(
            "-id"
        ).first()

        if last_staff:

            last_number = int(
                last_staff.employee_id.replace(
                    "EMP",
                    ""
                )
            )

            employee_id = f"EMP{last_number + 1:03d}"

        else:

            employee_id = "EMP001"

        # ------------------------------------------------
        # Create Staff record
        # ------------------------------------------------

        Staff.objects.create(
            employee_id=employee_id,
            first_name=teacher.user.first_name,
            last_name=teacher.user.last_name,
            gender=gender,
            role="Teacher",
            qualification=qualification,
            experience=int(experience),
            phone=teacher.phone,
            email=teacher.user.email,
            joining_date=joining_date,
            salary=salary,
            address=address,
            is_active=True,
        )

        # ------------------------------------------------
        # Approve Teacher
        # ------------------------------------------------

        teacher.is_approved = True

        teacher.approved_by = request.user

        teacher.approved_at = timezone.now()

        teacher.save()

        messages.success(
            request,
            "Teacher approved successfully.",
        )

        return redirect(
            "pending_teachers"
        )

    return render(
        request,
        "accounts/approve_teacher.html",
        {
            "teacher": teacher,
        },
    )


# ============================================================
# REJECT TEACHER
# ============================================================

@staff_member_required
def reject_teacher(request, user_id):

    teacher = get_object_or_404(
        UserProfile,
        user_id=user_id,
    )

    teacher.user.delete()

    messages.success(
        request,
        "Teacher rejected successfully.",
    )

    return redirect(
        "pending_teachers"
    )
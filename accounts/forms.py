from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


# ============================================================
# LOGIN FORM
# ============================================================

class LoginForm(AuthenticationForm):

    ROLE_CHOICES = [
        ("Principal", "Principal"),
        ("Teacher", "Teacher"),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "role-radio",
            }
        ),
        label="Login As",
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )

    def clean(self):

        cleaned_data = super().clean()

        # Role is only used after Django authenticates
        # username and password.
        return cleaned_data


# ============================================================
# USER FORM
# ============================================================

class UserForm(forms.ModelForm):

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ]

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }


# ============================================================
# USER PROFILE FORM
# ============================================================

class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            "role",
            "phone",
            "profile_image",
        ]

        widgets = {

            "role": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

        }


# ============================================================
# SIGNUP FORM
# ============================================================

class SignupForm(UserCreationForm):

    ROLE_CHOICES = [
        ("Principal", "Principal"),
        ("Teacher", "Teacher"),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "role-radio",
            }
        ),
        label="Register As",
    )

    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last Name",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email Address",
            }
        ),
    )

    mobile = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Mobile Number",
                "maxlength": "10",
                "inputmode": "numeric",
            }
        ),
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "autocomplete": "username",
            }
        ),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "new-password",
            }
        ),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
            }
        ),
    )

    class Meta:

        model = User

        fields = (
            "role",
            "first_name",
            "last_name",
            "mobile",
            "email",
            "username",
            "password1",
            "password2",
        )


# ============================================================
# FORGOT PASSWORD
# ============================================================

class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your registered email",
                "autocomplete": "email",
            }
        )
    )


# ============================================================
# RESET PASSWORD
# ============================================================

class ResetPasswordForm(forms.Form):

    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm new password",
            }
        ),
    )

    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:

            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data


# ============================================================
# OTP VERIFICATION
# ============================================================

class OTPVerificationForm(forms.Form):

    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter 6-digit OTP",
                "autocomplete": "one-time-code",
                "maxlength": "6",
                "inputmode": "numeric",
            }
        ),
    )

    def clean_otp(self):

        otp = self.cleaned_data["otp"]

        if not otp.isdigit():

            raise forms.ValidationError(
                "OTP must contain only numbers."
            )

        return otp
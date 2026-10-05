from django import forms
from .models import AdmissionEnquiry


class AdmissionEnquiryForm(forms.ModelForm):

    class Meta:
        model = AdmissionEnquiry

        fields = [
            "student_name",
            "parent_name",
            "phone",
            "email",
            "gender",
            "date_of_birth",
            "applying_for_class",
            "address",
            "message",
        ]

        widgets = {
            "student_name": forms.TextInput(attrs={"class": "form-control"}),
            "parent_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "applying_for_class": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }
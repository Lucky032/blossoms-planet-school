from django import forms

from .models import Student, SchoolClass, AcademicYear, Section, Subject, TeacherAssignment


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            "admission_number",
            "photo",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "academic_year",
            "school_class",
            "section",
            "father_name",
            "mother_name",
            "phone",
            "email",
            "address",
            "admission_date",
            "is_active",
        ]

        widgets = {
            "admission_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "academic_year": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "school_class": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "section": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "father_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "mother_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "admission_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean_photo(self):

        photo = self.cleaned_data.get("photo")

        # Existing image / no new upload
        if not photo or not hasattr(photo, "content_type"):
            return photo

        # Maximum file size: 2 MB
        if photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError(
                "Image size must be less than 2 MB."
            )

        # Allowed image types
        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/jpg",
        ]

        if photo.content_type not in allowed_types:
            raise forms.ValidationError(
                "Only JPG, JPEG and PNG images are allowed."
            )

        return photo


class SchoolClassForm(forms.ModelForm):

    class Meta:
        model = SchoolClass

        fields = [
            "name",
            "display_order",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Class 1",
                }
            ),

            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "1",
                }
            ),
        }


class AcademicYearForm(forms.ModelForm):

    class Meta:
        model = AcademicYear

        fields = [
            "name",
            "start_date",
            "end_date",
            "is_current",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 2026-2027",
                }
            ),

            "start_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "is_current": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                "End date cannot be earlier than start date."
            )

        return cleaned_data

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["school_class", "name"]

        widgets = {
            "school_class": forms.Select(
                attrs={"class": "form-select"}
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: A"
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            return name.strip().upper()
        return name


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "code"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Mathematics"
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: MATH101"
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            return name.strip()
        return name

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if code:
            return code.strip().upper()
        return code

class TeacherAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeacherAssignment
        fields = [
            "teacher",
            "subject",
            "school_class",
            "section",
            "academic_year",
        ]

        widgets = {
            "teacher": forms.Select(
                attrs={"class": "form-select"}
            ),
            "subject": forms.Select(
                attrs={"class": "form-select"}
            ),
            "school_class": forms.Select(
                attrs={"class": "form-select"}
            ),
            "section": forms.Select(
                attrs={"class": "form-select"}
            ),
            "academic_year": forms.Select(
                attrs={"class": "form-select"}
            ),
        }

class TeacherAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeacherAssignment
        fields = [
            "teacher",
            "subject",
            "school_class",
            "section",
            "academic_year",
        ]

        widgets = {
            "teacher": forms.Select(
                attrs={"class": "form-select"}
            ),
            "subject": forms.Select(
                attrs={"class": "form-select"}
            ),
            "school_class": forms.Select(
                attrs={"class": "form-select"}
            ),
            "section": forms.Select(
                attrs={"class": "form-select"}
            ),
            "academic_year": forms.Select(
                attrs={"class": "form-select"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["teacher"].queryset = (
            self.fields["teacher"].queryset
            .filter(
                role="Teacher",
                is_active=True
            )
            .order_by(
                "first_name",
                "last_name"
            )
        )
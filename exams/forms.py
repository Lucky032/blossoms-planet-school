from django import forms
from academics.models import SchoolClass, Subject, TeacherAssignment
from .models import Exam, Grade, ExamSubject, StudentMark


class DateInput(forms.DateInput):
    input_type = "date"


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            "name",
            "academic_year",
            "term",
            "start_date",
            "end_date",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "academic_year": forms.Select(attrs={"class": "form-select"}),
            "term": forms.Select(attrs={"class": "form-select"}),
            "start_date": DateInput(attrs={"class": "form-control"}),
            "end_date": DateInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and end < start:
            raise forms.ValidationError(
                "End date cannot be earlier than the start date."
            )

        return cleaned_data


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = [
            "grade_name",
            "minimum_percentage",
            "maximum_percentage",
        ]

        widgets = {
            "grade_name": forms.TextInput(attrs={"class": "form-control"}),
            "minimum_percentage": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "maximum_percentage": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }


class ExamSubjectForm(forms.ModelForm):
    class Meta:
        model = ExamSubject
        fields = [
            "exam",
            "school_class",
            "subject",
            "maximum_marks",
            "passing_marks",
        ]

        widgets = {
            "exam": forms.Select(attrs={"class": "form-select"}),
            "school_class": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.Select(attrs={"class": "form-select"}),
            "maximum_marks": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "passing_marks": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
        }


class StudentMarkForm(forms.ModelForm):
    class Meta:
        model = StudentMark
        fields = [
            "student",
            "exam_subject",
            "obtained_marks",
            "remarks",
        ]

        widgets = {
            "student": forms.Select(attrs={"class": "form-select"}),
            "exam_subject": forms.Select(attrs={"class": "form-select"}),
            "obtained_marks": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "remarks": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()

        exam_subject = cleaned_data.get("exam_subject")
        obtained_marks = cleaned_data.get("obtained_marks")

        if exam_subject and obtained_marks is not None:
            if obtained_marks > exam_subject.maximum_marks:
                raise forms.ValidationError(
                    f"Marks cannot exceed {exam_subject.maximum_marks}."
                )

        return cleaned_data


class MarksEntryFilterForm(forms.Form):

    exam = forms.ModelChoiceField(
        queryset=Exam.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    school_class = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if user and hasattr(user, "userprofile"):

            if user.userprofile.role == "Teacher":

                assignments = TeacherAssignment.objects.filter(
                    teacher__user=user
                ).select_related(
                    "academic_year",
                    "school_class",
                    "subject",
                )

                # Only assigned classes
                self.fields["school_class"].queryset = (
                    SchoolClass.objects.filter(
                        id__in=assignments.values_list(
                            "school_class_id",
                            flat=True,
                        )
                    )
                    .distinct()
                    .order_by("display_order")
                )

                # Only assigned subjects
                self.fields["subject"].queryset = (
                    Subject.objects.filter(
                        id__in=assignments.values_list(
                            "subject_id",
                            flat=True,
                        )
                    )
                    .distinct()
                    .order_by("name")
                )

                # Only exams belonging to assigned academic years
                self.fields["exam"].queryset = (
                    Exam.objects.filter(
                        academic_year_id__in=assignments.values_list(
                            "academic_year_id",
                            flat=True,
                        )
                    )
                    .distinct()
                    .order_by("-start_date")
                )

class StudentMarkEditForm(forms.ModelForm):
    class Meta:
        model = StudentMark
        fields = [
            "obtained_marks",
            "remarks",
        ]

        widgets = {
            "obtained_marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "remarks": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

from academics.models import SchoolClass

class RankingFilterForm(forms.Form):
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )

    school_class = forms.ModelChoiceField(
        queryset=SchoolClass.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={"class": "form-select"}
        ),
    )
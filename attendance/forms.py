from django import forms

from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:

        model = Attendance

        fields = [

            "student",

            "date",

            "status",

            "remarks",

        ]

        widgets = {

            "date": forms.DateInput(

                attrs={

                    "type": "date",

                    "class": "form-control",

                }

            ),

            "status": forms.Select(

                attrs={

                    "class": "form-select",

                }

            ),

            "student": forms.Select(

                attrs={

                    "class": "form-select",

                }

            ),

            "remarks": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 3,

                }

            ),

        }
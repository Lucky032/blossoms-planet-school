from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            "title",
            "event_date",
            "event_time",
            "venue",
            "description",
            "cover_image",
            "is_active",
        ]

        widgets = {
            "event_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "event_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
        }
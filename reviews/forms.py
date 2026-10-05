from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            "name",
            "designation",
            "review",
            "rating",
            "photo",
            "display_order",
            "is_active",
        ]

        widgets = {
            "review": forms.Textarea(
                attrs={"rows": 4}
            ),
            "rating": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 5,
                }
            ),
        }
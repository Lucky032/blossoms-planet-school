from django import forms

from .models import FeeCollection, FeeStructure


class FeeStructureForm(forms.ModelForm):

    class Meta:

        model = FeeStructure

        fields = [
            "school_class",
            "fee_type",
            "amount",
            "description",
        ]

        widgets = {

            "school_class": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "fee_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Description",
                }
            ),
        }

    def clean_amount(self):

        amount = self.cleaned_data.get("amount")

        if amount is not None and amount < 0:
            raise forms.ValidationError(
                "Fee amount cannot be negative."
            )

        return amount


class FeeCollectionForm(forms.ModelForm):

    class Meta:

        model = FeeCollection

        fields = [
            "student",
            "fee_structure",
            "amount_paid",
            "discount",
            "fine",
            "payment_mode",
            "payment_date",
            "receipt_number",
            "remarks",
        ]

        widgets = {

            "student": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "fee_structure": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "amount_paid": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "discount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "fine": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "payment_mode": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "payment_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "receipt_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Receipt Number",
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Remarks",
                }
            ),
        }

    def clean_amount_paid(self):

        amount_paid = self.cleaned_data.get("amount_paid")

        if amount_paid is not None and amount_paid < 0:
            raise forms.ValidationError(
                "Amount paid cannot be negative."
            )

        return amount_paid

    def clean_discount(self):

        discount = self.cleaned_data.get("discount")

        if discount is not None and discount < 0:
            raise forms.ValidationError(
                "Discount cannot be negative."
            )

        return discount

    def clean_fine(self):

        fine = self.cleaned_data.get("fine")

        if fine is not None and fine < 0:
            raise forms.ValidationError(
                "Fine cannot be negative."
            )

        return fine

    def clean(self):

        cleaned_data = super().clean()

        student = cleaned_data.get("student")
        fee_structure = cleaned_data.get("fee_structure")

        if student and fee_structure:

            if (
                fee_structure.school_class
                and student.school_class_id
                != fee_structure.school_class_id
            ):
                raise forms.ValidationError(
                    "The selected fee structure does not belong to the student's class."
                )

        return cleaned_data
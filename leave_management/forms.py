from django import forms

from .models import Leave


class LeaveForm(forms.ModelForm):
    """
    Form for employees to apply for leave.
    """

    class Meta:
        model = Leave
        fields = [
            "leave_type",
            "start_date",
            "end_date",
            "reason",
        ]

        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Enter the reason for leave",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError(
                    "End date cannot be earlier than start date."
                )

        return cleaned_data
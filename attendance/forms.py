from django import forms

from .models import Attendance


class AttendanceForm(forms.ModelForm):
    """
    Form for creating and updating attendance records.
    """

    class Meta:
        model = Attendance

        fields = [
            "employee",
            "date",
            "check_in",
            "check_out",
            "status",
            "remarks",
        ]

        widgets = {
            "employee": forms.Select(
                attrs={"class": "form-select"}
            ),

            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "check_in": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "check_out": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "status": forms.Select(
                attrs={"class": "form-select"}
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Enter remarks (optional)",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out:
            if check_out <= check_in:
                raise forms.ValidationError(
                    "Check-out time must be later than check-in time."
                )

        return cleaned_data
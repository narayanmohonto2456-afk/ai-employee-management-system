from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee

        fields = [
            "employee_id",
            "user",
            "department",
            "designation",
            "gender",
            "date_of_birth",
            "joining_date",
            "address",
            "city",
            "state",
            "country",
            "profile_picture",
        ]

        widgets = {

            "employee_id": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Employee ID"
            }),

            "user": forms.Select(attrs={
                "class": "form-select"
            }),

            "department": forms.Select(attrs={
                "class": "form-select"
            }),

            "designation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Designation"
            }),

            "gender": forms.Select(attrs={
                "class": "form-select"
            }),

            "date_of_birth": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "joining_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "country": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "profile_picture": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

        }

    def clean_employee_id(self):
        """
        Validate that the employee ID is unique.
        """

        employee_id = self.cleaned_data.get("employee_id")

        if Employee.objects.filter(
            employee_id=employee_id
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "Employee ID already exists."
            )

        return employee_id

    def clean_designation(self):
        """
        Validate designation field.
        """

        designation = self.cleaned_data.get("designation")

        if len(designation.strip()) < 2:
            raise forms.ValidationError(
                "Designation must contain at least 2 characters."
            )

        return designation

    def clean_city(self):
        """
        Validate city field.
        """

        city = self.cleaned_data.get("city")

        if len(city.strip()) < 2:
            raise forms.ValidationError(
                "Enter a valid city."
            )

        return city

    def clean_state(self):
        """
        Validate state field.
        """

        state = self.cleaned_data.get("state")

        if len(state.strip()) < 2:
            raise forms.ValidationError(
                "Enter a valid state."
            )

        return state

    def clean_country(self):
        """
        Validate country field.
        """

        country = self.cleaned_data.get("country")

        if len(country.strip()) < 2:
            raise forms.ValidationError(
                "Enter a valid country."
            )

        return country

    def clean(self):
        """
        Perform form-wide validation.
        """

        cleaned_data = super().clean()

        dob = cleaned_data.get("date_of_birth")
        joining_date = cleaned_data.get("joining_date")

        if dob and joining_date:
            if joining_date <= dob:
                raise forms.ValidationError(
                    "Joining date must be later than the date of birth."
                )

        return cleaned_data
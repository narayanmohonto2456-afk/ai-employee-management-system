from django import forms

from .models import Department


class DepartmentForm(forms.ModelForm):
    """
    Form used to create and update departments.
    """

    class Meta:
        model = Department

        fields = (
            "department_name",
            "department_code",
            "description",
        )

        widgets = {
            "department_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter department name",
                }
            ),

            "department_code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter department code",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter description",
                }
            ),
        }
    def clean_department_name(self):
        name = self.cleaned_data["department_name"].strip().title()

        queryset = Department.objects.filter(
            department_name=name
        )

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(
                "Department name already exists."
            )

        return name

    def clean_department_code(self):
        code = self.cleaned_data["department_code"].strip().upper()

        queryset = Department.objects.filter(department_code=code)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(
                "Department code already exists."
            )

        return code
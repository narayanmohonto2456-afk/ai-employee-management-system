from django import forms
from django.contrib.auth import get_user_model

from .models import Employee


User = get_user_model()


class EmployeeForm(forms.ModelForm):
    """
    Form for creating and updating employees.

    On creation:
        - Creates the related User automatically.
        - Assigns the EMPLOYEE role.
        - Uses email as the login identifier.
        - Hashes the initial password.

    On update:
        - Updates the related User's name and email.
        - Changes the password only when a new password is provided.
    """

    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last Name",
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "employee@gmail.com",
            }
        ),
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Initial password",
            }
        ),
    )

    class Meta:
        model = Employee

        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "employee_id",
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
            "employee_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Employee ID",
                }
            ),

            "department": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "designation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Designation",
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

            "joining_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Full address",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "State",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Country",
                }
            ),

            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    # ==========================================================
    # EMPLOYEE ID
    # ==========================================================

    def clean_employee_id(self):
        employee_id = self.cleaned_data.get("employee_id")

        if (
            Employee.objects
            .filter(employee_id=employee_id)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError(
                "Employee ID already exists."
            )

        return employee_id

    # ==========================================================
    # EMAIL
    # ==========================================================

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            return email

        email = email.strip().lower()

        existing_user = (
            User.objects
            .filter(email__iexact=email)
            .first()
        )

        if existing_user:

            # Creating a new employee
            if not self.instance.pk:
                raise forms.ValidationError(
                    "This email address is already registered."
                )

            # Updating an employee
            if (
                hasattr(self.instance, "user")
                and existing_user.pk != self.instance.user.pk
            ):
                raise forms.ValidationError(
                    "This email address is already registered."
                )

        return email

    # ==========================================================
    # PASSWORD
    # ==========================================================

    def clean_password(self):
        password = self.cleaned_data.get("password")

        # Password is required when creating
        # a new employee.
        if not self.instance.pk and not password:
            raise forms.ValidationError(
                "Initial password is required when creating an employee."
            )

        return password

    # ==========================================================
    # DESIGNATION
    # ==========================================================

    def clean_designation(self):
        designation = self.cleaned_data.get("designation")

        if designation and len(designation.strip()) < 2:
            raise forms.ValidationError(
                "Designation must contain at least 2 characters."
            )

        return designation.strip()

    # ==========================================================
    # CITY
    # ==========================================================

    def clean_city(self):
        city = self.cleaned_data.get("city")

        if city and len(city.strip()) < 2:
            raise forms.ValidationError(
                "Enter a valid city."
            )

        return city.strip()

    # ==========================================================
    # STATE
    # ==========================================================

    def clean_state(self):
        state = self.cleaned_data.get("state")

        if state and len(state.strip()) < 2:
            raise forms.ValidationError(
                "Enter a valid state."
            )

        return state.strip()

    # ==========================================================
    # COUNTRY
    # ==========================================================

    def clean_country(self):
        country = self.cleaned_data.get("country")

        if country and len(country.strip()) < 2:
            raise forms.ValidationError(
                "Enter a valid country."
            )

        return country.strip()

    # ==========================================================
    # FORM-WIDE VALIDATION
    # ==========================================================

    def clean(self):
        cleaned_data = super().clean()

        dob = cleaned_data.get("date_of_birth")
        joining_date = cleaned_data.get("joining_date")

        if dob and joining_date:

            if joining_date <= dob:
                raise forms.ValidationError(
                    "Joining date must be later than the date of birth."
                )

        return cleaned_data

    # ==========================================================
    # SAVE
    # ==========================================================

    def save(self, commit=True):
        """
        Create/update the Employee and its related User.
        """

        employee = super().save(commit=False)

        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data.get("password")

        # ======================================================
        # CREATE USER
        # ======================================================

        if not employee.pk:

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.EMPLOYEE,
                email_verified=False,
            )

            employee.user = user

            if commit:
                employee.save()
                self.save_m2m()

            return employee

        # ======================================================
        # UPDATE EXISTING USER
        # ======================================================

        user = employee.user

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        # Keep username synchronized with email.
        user.username = email

        # Only change password when one was supplied.
        if password:
            user.set_password(password)

        user.save()

        if commit:
            employee.save()
            self.save_m2m()

        return employee
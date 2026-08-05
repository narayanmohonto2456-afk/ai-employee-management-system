from django.contrib.auth.mixins import UserPassesTestMixin


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Allow only Admin users.
    """

    def test_func(self):
        return self.request.user.role == "ADMIN"


class HRRequiredMixin(UserPassesTestMixin):
    """
    Allow Admin and HR users.
    """

    def test_func(self):
        return self.request.user.role in [
            "ADMIN",
            "HR",
        ]


class EmployeeRequiredMixin(UserPassesTestMixin):
    """
    Allow all authenticated users.
    """

    def test_func(self):
        return self.request.user.is_authenticated
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


class AdminRequiredMixin(UserPassesTestMixin):
    """
    Allow only authenticated Admin users.
    """

    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and user.is_active
            and getattr(user, "role", None) == "ADMIN"
        )


class HRRequiredMixin(UserPassesTestMixin):
    """
    Allow authenticated Admin and HR users.
    """

    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and user.is_active
            and getattr(user, "role", None) in {
                "ADMIN",
                "HR",
            }
        )


class EmployeeRequiredMixin(UserPassesTestMixin):
    """
    Allow any authenticated and active user.
    """

    def test_func(self):
        user = self.request.user

        return (
            user.is_authenticated
            and user.is_active
        )


class NoCacheMixin:
    """
    Prevent protected pages from being cached by the browser.
    """

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
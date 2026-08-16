from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Authenticated users can read.

    Only Admin users can:
    - Create
    - Update
    - Partially update
    - Delete.
    """

    def has_permission(self, request, view):

        user = request.user

        if not user.is_authenticated or not user.is_active:
            return False

        if request.method in SAFE_METHODS:
            return True

        return getattr(user, "role", None) == "ADMIN"


class IsAdminOrHR(BasePermission):
    """
    Authenticated users can read employee data.

    Admin and HR users can:
    - Create
    - Update
    - Partially update

    Only Admin users can:
    - Delete
    """

    def has_permission(self, request, view):

        user = request.user

        if not user.is_authenticated or not user.is_active:
            return False

        if request.method in SAFE_METHODS:
            return True

        role = getattr(user, "role", None)

        if request.method in ("POST", "PUT", "PATCH"):
            return role in ("ADMIN", "HR")

        if request.method == "DELETE":
            return role == "ADMIN"

        return False
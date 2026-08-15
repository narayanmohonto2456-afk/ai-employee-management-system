from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Allow authenticated users to read.

    Only authenticated Admin users can:
    - Create
    - Update
    - Partially update
    - Delete
    """

    def has_permission(self, request, view):

        user = request.user

        # User must be authenticated and active.
        if not user.is_authenticated or not user.is_active:
            return False

        # All authenticated users can read.
        if request.method in SAFE_METHODS:
            return True

        # Only Admin users can modify data.
        return getattr(user, "role", None) == "ADMIN"
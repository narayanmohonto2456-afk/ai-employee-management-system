from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Allow everyone to read.
    Only staff users can create, update or delete.
    """

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff
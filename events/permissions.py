from rest_framework.compat import is_authenticated
from rest_framework import permissions



class IsAuthenticatedOrPostOnly(permissions.BasePermission):
    """
        global permission to allow only post method for unauthorized users
    """

    def has_permission(self, request, view):
        # need a better way to do this
        if request.method  == 'POST':
            return True
        else:
            return request.user and is_authenticated(request.user)



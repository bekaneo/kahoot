from rest_framework.permissions import BasePermission

from questions.models import Test


class IsUserGroup(BasePermission):
    def has_permission(self, request, view):
        test = request.get_full_path().split('/')[2]
        if Test.objects.filter(title=test).exists():
            group = Test.objects.get(title=test).group
            return group == request.user.group
        return True



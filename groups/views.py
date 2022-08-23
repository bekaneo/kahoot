from rest_framework.viewsets import ModelViewSet

from groups.serializers import GroupSerializer
from .models import Group


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

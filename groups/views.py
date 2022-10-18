from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend


from groups.serializers import GroupSerializer
from .models import Group


class ListGroupView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    permission_classes = [AllowAny]

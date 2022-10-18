from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
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

    # def get(self, request):
    #     serializer = GroupSerializer(self.get_queryset(), many=True)
    #     if serializer.data:
    #         data = sorted(serializer.data, key=lambda x: x.get('score'), reverse=True)
    #         return Response(data, status=status.HTTP_200_OK)

    #     return Response('Not Found Groups', status=status.HTTP_404_NOT_FOUND)
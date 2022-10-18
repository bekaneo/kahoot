from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from groups.serializers import GroupSerializer
from .models import Group


class ListGroupView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = GroupSerializer(self.get_queryset(), many=True)
        if serializer.data:
            # data = sorted(serializer.data, key=lambda x: x['score'], reverse=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response('Not Found Groups', status=status.HTTP_404_NOT_FOUND)
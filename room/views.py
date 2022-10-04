from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from room.models import Room, RoomUsers
from room.serializers import CreateRoomSerializer, RetrieveRoomSerializer, AddUserRoomSerializer


class CreateRoomView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateRoomSerializer

    @swagger_auto_schema(request_body=CreateRoomSerializer)
    def create(self, request, *args, **kwargs):
        serializer = CreateRoomSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            queryset = Room.objects.get(**serializer.data)
            return Response({'code': queryset.code}, status=status.HTTP_201_CREATED)

        return Response('Not Valid Data', status=status.HTTP_400_BAD_REQUEST)


class RetrieveRoomView(RetrieveAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveRoomSerializer

    def retrieve(self, request, code, *args, **kwargs):
        if not Room.objects.filter(code=code).exists():
            return Response('Room with this code was not found', status=status.HTTP_400_BAD_REQUEST)
        room = Room.objects.get(code=code)
        queryset = RoomUsers.objects.filter(room=room)
        serializer = RetrieveRoomSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AddUserRoomSerializer)
    def create(self, request, code, *args, **kwargs):
        data = {'code': code}
        serializer = AddUserRoomSerializer(data=data, context={'request': request, 'code': code})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Success', status=status.HTTP_201_CREATED)

        return Response('Not Valid Data', status=status.HTTP_400_BAD_REQUEST)




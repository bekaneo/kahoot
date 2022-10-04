from django.utils.crypto import get_random_string
from rest_framework import serializers

from room.models import Room, RoomUsers
from questions.models import Test


class CreateRoomSerializer(serializers.Serializer):
    test = serializers.CharField()
    name = serializers.CharField()
    host = serializers.ReadOnlyField(source='user.login')

    def validate_test(self, test):
        if not Test.objects.filter(title=test).exists():
            raise serializers.ValidationError('Test Does Not Exist')
        return Test.objects.get(title=test)

    def validate(self, attrs):
        attrs['host'] = self.context.get('request').user
        attrs['code'] = get_random_string(10)
        return super().validate(attrs)

    def create(self, validated_data):
        try:
            room = Room.objects.get(host=validated_data['host'], test=validated_data['test'])
            room.delete()
            return Room.objects.create(**validated_data)
        except Room.DoesNotExist:
            return Room.objects.create(**validated_data)


class RetrieveRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomUsers
        fields = '__all__'


class AddUserRoomSerializer(serializers.Serializer):

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['code'] = self.context.get('code')
        attrs['room'] = Room.objects.get(code=attrs['code'])
        attrs['user'] = self.context.get('request').user

        if not Room.objects.filter(code=attrs['code']).exists():
            raise serializers.ValidationError('Code is not valid')

        if RoomUsers.objects.filter(**attrs).exists():
            raise serializers.ValidationError('User already in this room')

        return attrs

    def create(self, validated_data):
        return RoomUsers.objects.create(**validated_data)

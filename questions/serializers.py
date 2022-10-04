from rest_framework import serializers

from accounts.models import User
from questions.models import Test, Question, Answer


class TestUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

    def to_representation(self, instance):
        passed_users = instance.score.all().order_by('-score')
        users = []
        for user in passed_users:
            user = User.objects.get(login=user.login)
            serializer = UserSerializer(user, context={'test': instance})
            users.append(serializer.data)
        representation = super().to_representation(instance)
        representation['leaders'] = users
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'second_name', 'phone_number', 'login']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['score'] = instance.score.get(login=instance, test=self.context.get('test')).score
        representation['rating'] = instance.rating.get(login=instance, test=self.context.get('test')).rating
        representation['test_passed'] = instance.score.count()
        return representation


class RetrieveQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['answers'] = AnswersSerializer(instance.answer.all(), many=True).data
        return representation


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['A', 'B', 'C', 'D']


class AnswerSerializer(serializers.ModelSerializer):
    answer = serializers.CharField()
    time = serializers.IntegerField()

    class Meta:
        model = Answer
        fields = '__all__'

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)


class ListQuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['answers'] = AnswersSerializer(instance.answer.all(), many=True).data
        return representation

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)


class ListTestSerializer(serializers.ModelSerializer):
    questions = ListQuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['questions_count'] = instance.questions.count()
        representation['test_passed'] = instance.score.count()
        return representation

    def to_internal_value(self, data):
        values = super().to_internal_value(data)
        print(values)
        print(data)
        return super().to_internal_value(data)

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

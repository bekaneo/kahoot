from rest_framework import serializers

from accounts.models import User
from groups.models import Group
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


class ListQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['answers'] = AnswersSerializer(instance.answer.all(), many=True).data
        return representation


class ListTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['questions_count'] = instance.questions.count()
        representation['test_passed'] = instance.score.count()
        return representation


class CreateAnswerSerializer(serializers.Serializer):
    A = serializers.CharField(max_length=100)
    B = serializers.CharField(max_length=100)
    C = serializers.CharField(max_length=100)
    D = serializers.CharField(max_length=100)
    correct_answer = serializers.CharField(max_length=10)

    def create(self, validated_data):
        validated_data['question'] = self.context.get('question')
        answer = Answer.objects.create(**validated_data)
        return answer


class CreateQuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=100)
    score = serializers.IntegerField(default=100)
    timer = serializers.IntegerField(default=20)
    image = serializers.ImageField(required=False)
    answers = CreateAnswerSerializer()

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        validated_data['test'] = self.context.get('test')
        question = Question.objects.create(**validated_data)
        a_serializer = CreateAnswerSerializer(data=answers, context={'question': question})
        if a_serializer.is_valid(raise_exception=True):
            a_serializer.save()
        return question


class CreateTestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    image = serializers.ImageField(required=False)
    questions = CreateQuestionSerializer(many=True)

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        validated_data['group'] = Group.objects.get(pk='zeon')
        test = Test.objects.create(**validated_data)
        q_serializer = CreateQuestionSerializer(data=questions, many=True, context={'test': test})
        if q_serializer.is_valid(raise_exception=True):
            q_serializer.save()
        return test

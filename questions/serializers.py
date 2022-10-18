from rest_framework import serializers

from accounts.models import Score, User, UserQuestionScore
from groups.models import Group
from questions.models import Test, Question, Answer
from questions.services import update_overall_score, update_test_rating, update_user_ratings


class TestUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

    def to_representation(self, instance):
        passed_users = instance.score.all().order_by('-score')
        users = []
        for user in passed_users:
            user = User.objects.filter(login=user.login)
            serializer = UserSerializer(user, many=True, context={'test': instance})
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
        print(instance)
        print(self.context.get('test'))
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
        exclude = ['question', 'correct_answer', 'id']


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
        representation['correct_answer'] = instance.answer.get().correct_answer
        representation['answers'] = AnswersSerializer(instance.answer.all(), many=True).data
        # print(representation)
        # print(Test.questions.get(question_id=representation['id']))
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
    description = serializers.CharField(max_length=500, required=False)
    questions = CreateQuestionSerializer(many=True)

    def validate_title(self, title):
        if Test.objects.filter(title=title).exists():
            raise serializers.ValidationError('Test with this title already exists')
        return title
    def create(self, validated_data):
        questions = validated_data.pop('questions')
        validated_data['group'] = Group.objects.get(pk='zeon')
        test = Test.objects.create(**validated_data)
        q_serializer = CreateQuestionSerializer(data=questions, many=True, context={'test': test})
        if q_serializer.is_valid(raise_exception=True):
            q_serializer.save()
        return test


class CreateRoundScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'
    
    def create(self, validated_data):
        user = validated_data['login']
        final_score = validated_data['score']
        test = validated_data['test']
        if Score.objects.filter(test=test, login=user).exists():
            Score.objects.filter(test=test, login=user).delete()
        score = Score.objects.create(**validated_data)
        update_overall_score(user, final_score)
        update_user_ratings(user)
        update_test_rating(test=test)
        return score


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['image']
    

from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from groups.models import Group
from kahoot import settings
from questions.models import Test, Question
from questions.serializers import AnswersSerializer

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_active', 'is_staff', 'activation_code', 'last_login']

    def to_representation(self, instance):
        tests = []
        test_rating = instance.rating.all()
        for rating in test_rating:
            test = rating.test
            serializer = UserTestSerializer(test, context={'user': instance})
            tests.append(serializer.data)
        representation = super().to_representation(instance)
        representation['passed_tests'] = instance.score.count()
        representation['tests'] = tests
        return representation


class UserTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['title', 'group']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context.get('user')
        questions = RetrieveQuestionSerializer(instance.questions.all(), many=True, context={'user': user})
        representation['score'] = instance.score.get(login=user, test=instance).score
        representation['rating'] = instance.rating.get(login=user, test=instance).rating
        representation['questions'] = questions.data
        return representation


class RetrieveQuestionSerializer(serializers.ModelSerializer):
    # answer = AnswersSerializer(many=True)
    class Meta:
        model = Question
        fields = '__all__'

    def to_representation(self, instance):
        user_answers = instance.q_score.filter(user=self.context.get('user'))
        user_answer = []
        user_score = []
        for user in user_answers:
            user_answer.append(user.answer)
            user_score.append(user.score)
        representation = super().to_representation(instance)
        representation['answers'] = AnswersSerializer(instance.answer.all(), many=True).data
        representation['user_answer'] = user_answer
        representation['user_score'] = user_score
        return representation


class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['login', 'name', 'second_name',
                  'group', 'phone_number', 'overall_score', 'overall_rating', 'group_rating']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['passed_tests'] = instance.score.count()
        return representation



class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    second_name = serializers.CharField()
    phone_number = serializers.CharField()
    group = serializers.CharField()
    password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)

    def validate_email(self, email):
        if User.objects.filter(login=email).exists():
            raise serializers.ValidationError('This email is already exists')
        return email

    def validate_group(self, group):
        try:
            group = Group.objects.get(name=group)
        except Group.DoesNotExist:
            raise serializers.ValidationError('Group Does Not Exist')
        return group

    def validate(self, attrs):
        attrs['login'] = attrs.pop('email')
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords are not identical')
        return super().validate(attrs)

    def create(self, **kwargs):
        User.objects.create_user(**self.validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    login = serializers.EmailField()
    password = serializers.CharField(min_length=4)

    def validate_login(self, login):
        if not User.objects.filter(login=login).exists():
            raise serializers.ValidationError('This email does not exists')
        return login

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        user = User.objects.get(login=login)
        if not user.check_password(password):
            raise serializers.ValidationError('Password is not valid')
        return super().validate(attrs)


class RestorePasswordSerializer(serializers.Serializer):
    login = serializers.EmailField()

    def validate_login(self, login):
        if not User.objects.filter(login=login).exists():
            raise serializers.ValidationError('This email does not exists')
        return login

    def send_verification_code(self):
        login = self.validated_data.get('login')
        user = User.objects.get(login=login)
        user.create_activation_code()
        send_mail(
            subject='Activation',
            message=f'Ваш код {user.activation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[login],
            fail_silently=False
        )


class RestorePasswordCompleteSerializer(serializers.Serializer):
    login = serializers.EmailField()
    activation_code = serializers.CharField(max_length=20, min_length=20)
    password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)

    def validate(self, attrs):
        login = attrs.get('login')
        code = attrs.get('activation_code')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords are not identical')
        if not User.objects.filter(login=login, activation_code=code).exists():
            raise serializers.ValidationError('User with this email and activation code not found')
        return super().validate(attrs)

    def set_new_password(self):
        print(self.validated_data)
        login = self.validated_data.get('login')
        password = self.validated_data.get('password')
        user = User.objects.get(login=login)
        user.set_password(password)
        user.save()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4)
    new_password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)

    def validate_old_password(self, password):
        user = self.context['request'].user
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid password')
        return password

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        password_confirm = attrs.get('password_confirm')
        if new_password != password_confirm:
            raise serializers.ValidationError('Passwords are not identical')
        return super().validate(attrs)

    def set_new_password(self):
        user = self.context['request'].user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()

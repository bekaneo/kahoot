from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string

from groups.models import Group
from questions.models import Test, Question


class UserManager(BaseUserManager):
    def _create(self, login, password, name, **fields):
        login = self.normalize_email(login)
        user = self.model(login=login, name=name, **fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, login, password, name, **fields):
        fields.setdefault('is_active', True)
        fields.setdefault('is_staff', False)
        return self._create(login, password, name, **fields)

    def create_superuser(self, login, password, name, **fields):
        fields.setdefault('is_active', True)
        fields.setdefault('is_staff', True)
        return self._create(login, password, name, **fields)


class User(AbstractBaseUser):
    name = models.CharField(max_length=50, blank=True)
    second_name = models.CharField(max_length=50, blank=True)
    login = models.EmailField(primary_key=True)
    phone_number = models.CharField(max_length=15, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='user')
    overall_score = models.IntegerField(blank=True, default=0)
    overall_rating = models.IntegerField(blank=True, default=0)
    group_rating = models.IntegerField(blank=True, default=0)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=5, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.login

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(5)
        self.activation_code = code
        self.save()
        return code

    def get_all_permissions(self, obj=None):
        return ''


class Score(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score')
    score = models.SmallIntegerField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='score')

    def __str__(self):
        return str(self.test)


class Rating(models.Model):
    login = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='rating')

    def __str__(self):
        return str(self.test)


class UserQuestionTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='q_time')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='q_time')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='q_time')
    time = models.CharField(max_length=100)


class UserQuestionScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='q_score')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='q_score')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='q_score')
    score = models.SmallIntegerField(blank=True)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return str(self.test)

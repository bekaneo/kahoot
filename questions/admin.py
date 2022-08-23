from django.contrib import admin
from django.db.models import Avg
from django.contrib.auth import get_user_model

import nested_admin

from .models import Test, Question, Answer


User = get_user_model()


class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    max_num = 1


class QuestionInLine(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline]
    min_num = 1


class TestAdmin(nested_admin.NestedModelAdmin):
    model = Test
    list_display = ['title', 'group', 'questions', 'passed', 'leader', 'leader_score', 'avg_score']
    inlines = [QuestionInLine]

    def questions(self, obj: Test):
        return obj.questions.count()

    def passed(self, obj: Test):
        return obj.score.count()

    def leader(self, obj: Test):
        if obj.rating.filter(rating__gt=0):
            return obj.rating.all().order_by('rating').first().login
        return '-'

    def leader_score(self, obj: Test):
        if obj.score.all():
            return obj.score.all().order_by('-score').first().score
        return '-'

    def avg_score(self, obj: Test):
        if obj.score.all():
            return obj.score.aggregate(Avg('score'))['score__avg']
        return '-'


admin.site.register(Test, TestAdmin)

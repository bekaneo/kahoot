import nested_admin
from django.contrib import admin
from django.db.models import Avg

from accounts.models import User, Score, UserQuestionScore


class QuestionInline(nested_admin.NestedStackedInline):
    model = UserQuestionScore
    readonly_fields = ['question', 'test', 'answer', 'score']
    verbose_name = 'User Answer'
    verbose_name_plural = 'User Answers'
    max_num = 0


class ScoreInLine(nested_admin.NestedStackedInline):
    model = Score
    readonly_fields = ['score', 'test']
    verbose_name = 'User Test'
    verbose_name_plural = 'User Test'
    max_num = 0


@admin.register(User)
class UserAdmin(nested_admin.NestedModelAdmin):
    model = User
    inlines = [ScoreInLine, QuestionInline]
    list_filter = ['group']
    list_display = ['login', 'name', 'second_name', 'phone_number',
                    'group', 'overall_rating', 'group_rating',
                    'overall_score']
    search_fields = ['name', 'second_name', 'phone_number']


class LeaderBoardProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Leaderboard'
        verbose_name_plural = 'Leaderboard'


@admin.register(LeaderBoardProxy)
class LeaderBoard(admin.ModelAdmin):
    inlines = [ScoreInLine, QuestionInline]
    list_display = ['login', 'name', 'second_name', 'group',
                    'phone_number', 'overall_score', 'overall_rating',
                    'passed', 'avg_score']
    list_filter = ['group']
    search_fields = ['name', 'second_name', 'phone_number']

    def passed(self, obj: User):
        return obj.score.count()

    def avg_score(self, obj: User):
        score = obj.score.aggregate(Avg('score'))['score__avg']
        return score

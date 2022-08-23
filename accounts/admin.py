from django.contrib import admin
from django.db.models import Avg

from accounts.models import User, Score, Rating


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_filter = ['group']
    list_display = ['login', 'name', 'second_name', 'phone_number', 'group', 'overall_rating', 'group_rating',
                    'avg_score', 'overall_score', 'passed']
    search_fields = ['name', 'second_name', 'phone_number']


    def avg_score(self, obj: User):
        score = obj.score.aggregate(Avg('score'))['score__avg']
        return score

    def passed(self, obj: User):
        return obj.score.count()


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    model = Score
    list_display = ['id', 'login', 'score', 'test']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ['id', 'login', 'rating', 'test']

from django.contrib import admin
from django.db.models import Avg

from groups.models import Group


@admin.register(Group)
class UserAdmin(admin.ModelAdmin):
    model = Group
    list_display = ['name', 'users', 'tests', 'avg_score', 'leader']

    def users(self, obj: Group):
        return obj.user.count()

    def tests(self, obj: Group):
        return obj.test.count()

    def avg_score(self, obj: Group):
        if obj.user.filter(overall_score__gt=0):
            return obj.user.filter(overall_score__gt=0).aggregate(Avg('overall_score'))['overall_score__avg']
        return '-'

    def leader(self, obj: Group):
        if obj.user.filter(overall_score__gt=0):
            return obj.user.filter(overall_score__gt=0).order_by('-overall_score').first().login
        return '-'

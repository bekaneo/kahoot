from datetime import datetime

from django.db.models import Sum, QuerySet
from django.contrib.auth import get_user_model
from rest_framework.request import Request

from accounts.models import UserQuestionScore, Score, Rating, UserQuestionTime
from questions.models import Test, Question

User = get_user_model()


def update_user_ratings(user: str) -> None:
    user = User.objects.get(login=user)
    all_user = User.objects.all().order_by('-overall_score')
    group_user = User.objects.filter(group=user.group).order_by('-overall_score')
    rating = 1
    for user in all_user:
        user.overall_rating = rating
        user.save()
        rating += 1
    rating = 1
    for user in group_user:
        user.group_rating = rating
        user.save()
        rating += 1


def update_overall_score(user: str, final_score: int) -> None:
    # user = User.objects.get(login=request.user)
    user = User.objects.get(login=user)
    user.overall_score += final_score
    user.save()


def create_final_score(request: Request, test: str) -> int:

    final_score = UserQuestionScore.objects.filter(test=test, user=request.user)
    final_score = final_score.aggregate(Sum('score'))['score__sum']
    # test = Test.objects.get(title=test)
    # try:
    #     user_score = Score.objects.get(login=request.user, test=test)
    #     user_score.score = final_score
    #     user_score.save()
    # except Score.DoesNotExist:
    #     Score.objects.create(login=request.user, test=test, score=final_score)

    update_test_rating(test)
    update_overall_score(request, final_score)
    update_user_ratings(request)

    return final_score


def update_test_rating(test: str) -> None:
    queryset = UserQuestionScore.objects.filter(test=test)
    queryset = queryset.values('user').annotate(final_score=Sum('score')).order_by('-final_score')
    ratings = Rating.objects.filter(test=test)
    ratings.delete()
    rating = 1
    for user in queryset:
        login = User.objects.get(login=user['user'])
        Rating.objects.create(rating=rating, test=test, login=login)
        rating += 1


def create_score(request: Request, question: QuerySet, score: int, test: str) -> None:
    answer = request.data.get('answer')
    test = Test.objects.get(title=test)
    try:
        user_question = UserQuestionScore.objects.get(user=request.user, question=question, test=test)
        user_question.score = score
        user_question.save()
    except UserQuestionScore.DoesNotExist:
        UserQuestionScore.objects.create(user=request.user, test=test, question=question,
                                         score=score, answer=answer)


def create_time(request: Request, question: str, test: str) -> None:
    question = Question.objects.get(id=question)
    test = Test.objects.get(title=test)
    try:
        user_question = UserQuestionTime.objects.get(user=request.user, question=question,test=test)
        user_question.time = datetime.now()
        user_question.save()
    except UserQuestionTime.DoesNotExist:
        UserQuestionTime.objects.create(user=request.user, test=test,
                                        question=question, time=datetime.now())

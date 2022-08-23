from datetime import datetime
from typing import Union

from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from rest_framework.request import Request

from accounts.models import UserQuestionScore, UserQuestionTime
from questions.models import Answer, Test, Question
from questions.services import create_final_score

User = get_user_model()


def validate_answer(request: Request, question_id: QuerySet) -> bool:
    answers = Answer.objects.get(question=question_id)
    answer = request.data.get('answer', None)
    if answer is not None:
        if answer == answers.correct_answer:
            return True
    return False


def calculate_score(request: Request, question_id: QuerySet) -> int:
    queryset = Question.objects.get(id=question_id)
    time = UserQuestionTime.objects.get(user=request.user, question=question_id).time
    calc_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    time_difference = int((datetime.now() - calc_time).total_seconds())

    if request.data.get('time'):
        time_difference = request.data.get('time')

    if time_difference > queryset.timer:
        return 0

    if validate_answer(request, question_id):
        return int(queryset.score - (queryset.score / queryset.timer * time_difference))
    return 0


def check_answers(request: Request, test: str) -> Union[bool, int]:
    test = Test.objects.get(title=test)
    total_questions = Test.objects.get(title=test).questions.count()
    answered_questions = UserQuestionScore.objects.filter(test=test, user=request.user).count()

    if total_questions == answered_questions:
        return create_final_score(request, test)

    return False

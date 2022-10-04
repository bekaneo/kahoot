from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from questions.models import Test, Question
from questions.permissions import IsUserGroup
from questions.serializers import (ListTestSerializer,
                                   ListQuestionSerializer,
                                   RetrieveQuestionSerializer,
                                   AnswerSerializer,
                                   TestUsersSerializer)

from questions.services import create_time, create_score
from questions.utils import calculate_score, check_answers


class ListTestView(ListAPIView, CreateAPIView):
    serializer_class = ListTestSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Test.objects.filter(group=request.user.group)
        serializer = ListTestSerializer(queryset, context={'request': request}, many=True)

        if not serializer.data:
            return Response('Not found tests', status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = ListTestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response('Not Valid', status=status.HTTP_400_BAD_REQUEST)
    # def create(self, request, *args, **kwargs):
    #     questions = request.data.pop('questions')
    #     test_serializer = ListTestSerializer(data=request.data, context={'request': request})
    #     if test_serializer.is_valid(raise_exception=True):
    #         test_serializer.save()
    #         # print(test_serializer.)
    #         for question in questions:
    #             answers = question.pop('answers')
    #             question_serializer = ListQuestionSerializer(data=question, many=True, context={'request': request})
    #             if question_serializer.is_valid(raise_exception=True):
    #                 question_serializer.save()
    #                 for answer in answers:
    #                     answer_serializer = AnswerSerializer(data=answer, many=True, context={'request': request})
    #                     if answer_serializer.is_valid(raise_exception=True):
    #                         answer_serializer.save()
    #     return Response('Offf', status=status.HTTP_200_OK)


class TestUsersView(ListAPIView):
    serializer_class = TestUsersSerializer
    permission_classes = []

    def list(self, request, test, *args, **kwargs):
        queryset = Test.objects.filter(title=test)
        serializer = TestUsersSerializer(queryset, many=True)

        if not serializer.data:
            return Response('Not found test', status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ListQuestionsView(RetrieveAPIView):
    serializer_class = ListQuestionSerializer
    permission_classes = [IsAuthenticated, IsUserGroup]

    def retrieve(self, request, test, *args, **kwargs):
        queryset = Question.objects.filter(test=test)
        serializer = ListQuestionSerializer(queryset, many=True)

        if not serializer.data:
            return Response(f'Not found this test {test}', status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveQuestionView(RetrieveAPIView, CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsUserGroup]

    def retrieve(self, request, test, question, *args, **kwargs):
        queryset = Question.objects.filter(id=question, test=test)
        serializer = RetrieveQuestionSerializer(queryset, many=True)

        if not serializer.data:
            return Response('Question not Found', status=status.HTTP_404_NOT_FOUND)

        create_time(request, question, test)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, test, question, *args, **kwargs):
        queryset = Question.objects.get(id=question)
        score = calculate_score(request, question)
        check_answer = check_answers(request, test)

        if check_answer:
            return Response(f'Test is over {check_answer}', status=status.HTTP_201_CREATED)

        create_score(request, queryset, score, test)
        return Response(f'Your score is {score}', status=status.HTTP_201_CREATED)

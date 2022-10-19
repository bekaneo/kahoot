from django.urls import is_valid_path
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from questions.paginations import StandardResultsSetPagination
from questions.models import Test, Question
from questions.permissions import IsUserGroup
from questions.serializers import (CreateRoundScoreSerializer, 
                                   ListTestSerializer,
                                   ListQuestionSerializer,
                                   TestSerializer,
                                   TestUsersSerializer, 
                                   CreateTestSerializer)

from questions.services import create_time, create_score
from questions.utils import calculate_score, check_answers

class CreateRoundScoreView(CreateAPIView):
    serializer_class = CreateRoundScoreSerializer
    permission_classes = [IsAuthenticated]
 
    def post(self, request, *args, **kwargs):
        serializer = CreateRoundScoreSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

class UpdateTestView(UpdateAPIView):
    serializer_class = TestSerializer

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class CreateTestView(CreateAPIView):
    serializer_class = CreateTestSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = CreateTestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.initial_data, status=status.HTTP_201_CREATED)

        return Response('Not Valid', status=status.HTTP_400_BAD_REQUEST)
    

class ListTestView(ListAPIView, CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = ListTestSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title']

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Test.objects.filter(group=self.request.user.group)

    @swagger_auto_schema(request_body=CreateRoundScoreSerializer(many=True))
    def post(self, request, *args, **kwargs):
        serializer = CreateRoundScoreSerializer(data=request.data, many=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)


class TestUsersView(ListAPIView):
    serializer_class = TestUsersSerializer
    permission_classes = []

    @swagger_auto_schema(request_body=TestUsersSerializer)
    def list(self, request, test, *args, **kwargs):
        
        queryset = Test.objects.filter(title=test)
        serializer = TestUsersSerializer(queryset, many=True)

        if not serializer.data:
            return Response('Not found test', status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class ListQuestionsView(RetrieveAPIView, UpdateAPIView):
    serializer_class = ListQuestionSerializer
    permission_classes = [IsAuthenticated, IsUserGroup]
    pagination_class = StandardResultsSetPagination
    queryset = Test.objects.all()

    def patch(self, request, test, *args, **kwargs):
        instance = Test.objects.get(title=test)
        serializer = TestSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, test, *args, **kwargs):
        queryset = Question.objects.filter(test=test)
        test_queryset = Test.objects.filter(title=test).first()
        serializer = ListQuestionSerializer(queryset, many=True)

        if not serializer.data:
            return Response(f'Not found this test {test}', status=status.HTTP_404_NOT_FOUND)
        test_serializer = ListTestSerializer(test_queryset)
        data = {
            'test': test_serializer.data,
            'questions': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


# class RetrieveQuestionView(RetrieveAPIView, CreateAPIView):
#     serializer_class = AnswerSerializer
#     permission_classes = [IsAuthenticated, IsUserGroup]
    

#     def retrieve(self, request, test, question, *args, **kwargs):
        
#         queryset = Question.objects.filter(id=question, test=test)
#         serializer = RetrieveQuestionSerializer(queryset, many=True)

#         if not serializer.data:
#             return Response('Question not Found', status=status.HTTP_404_NOT_FOUND)

#         create_time(request, question, test)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def create(self, request, test, question, *args, **kwargs):
#         queryset = Question.objects.get(id=question)
#         score = calculate_score(request, question)
#         check_answer = check_answers(request, test)

#         if check_answer:
#             return Response(f'Test is over {check_answer}', status=status.HTTP_201_CREATED)

#         create_score(request, queryset, score, test)
#         return Response(f'Your score is {score}', status=status.HTTP_201_CREATED)

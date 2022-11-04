from django.urls import path

from questions.views import (CreateRoundScoreView, 
                             ListTestView,
                             ListQuestionsView,
                             TestUsersView,
                             CreateTestView,
                             UpdateTestView,
                             UpdateTestImageView
                             )

                             
urlpatterns = [
    path('', ListTestView.as_view()),
    path('create', CreateTestView.as_view()),
    path('create/<str:test>', UpdateTestView.as_view()),
    path('<str:test>/', ListQuestionsView.as_view()),
    path('<str:test>/users', TestUsersView.as_view()),
    path('update/<str:test>', UpdateTestImageView.as_view())
]


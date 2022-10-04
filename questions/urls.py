from django.urls import path

from questions.views import (ListTestView,
                             ListQuestionsView,
                             RetrieveQuestionView,
                             TestUsersView)


urlpatterns = [
    path('', ListTestView.as_view()),
    path('<str:test>/', ListQuestionsView.as_view()),
    path('<str:test>/users', TestUsersView.as_view()),
    path('<str:test>/<int:question>', RetrieveQuestionView.as_view())
]


from django.urls import path

from room.views import CreateRoomView, RetrieveRoomView

urlpatterns = [
    path('', CreateRoomView.as_view()),
    path('<str:code>', RetrieveRoomView.as_view()),
]

from django.urls import path
from rest_framework.routers import DefaultRouter
from groups.views import ListGroupView

urlpatterns = [
    path('', ListGroupView.as_view())
]


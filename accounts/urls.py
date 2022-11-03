from django.urls import path

from .views import (RegistrationView,
                    LoginView,
                    UpdateTokenView,
                    LogoutView,
                    RestorePasswordView,
                    RestorePasswordCompleteView,
                    ChangePasswordView,
                    ProfileView,
                    UsersListView)


urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', UpdateTokenView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('restore_password/', RestorePasswordView.as_view()),
    path('restore_complete/', RestorePasswordCompleteView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('users/', UsersListView.as_view()),
    path('users/<str:user_id>', ProfileView.as_view())
]

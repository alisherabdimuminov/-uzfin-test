from django.urls import path

from .views import home, test, check_test, create_question
from users.views import create_user


urlpatterns = [
    path("", home, name="home"),
    path("test/<int:pk>/", test, name="test"),
    path("check_test/<int:pk>/", check_test, name="check"),
    path("create/question/", create_question, name="create_question"),
    path("create/user/", create_user, name="create_user"),
]

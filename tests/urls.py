from django.urls import path

from .views import home, test, check_test, create_question


urlpatterns = [
    path("", home, name="home"),
    path("test/<int:pk>/", test, name="test"),
    path("check_test/<int:pk>/", check_test, name="check"),
    path("create/", create_question, name="create_question"),
]

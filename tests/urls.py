from django.urls import path

from .views import home, test, check_test


urlpatterns = [
    path("", home, name="home"),
    path("test/<int:pk>/", test, name="test"),
    path("check_test/<int:pk>/", check_test, name="check"),
]

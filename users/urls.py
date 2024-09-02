from django.urls import path

from .views import login_handler
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", login_handler, name='login'),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout")
]

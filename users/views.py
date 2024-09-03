import random
import string
from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .models import User


def login_handler(request: HttpRequest):
    errors = None
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username") or "username"
        password = request.POST.get("password") or "password"
        user = authenticate(request, username=username, password=password)
        if user:
            login(request=request, user=user)
            return redirect("home")
        else:
            errors = "Foydalanuvchi nomi yokida parol xato!"
    return render(request, "login.html", {
        "errors": errors
    })


def gen_pass():
    password = ""
    for i in range(8):
        password += random.choice(string.ascii_letters + string.digits)
    return password


@csrf_exempt
def create_user(request: HttpRequest):
    password = gen_pass()
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    state = request.POST.get("state")
    username = str(first_name).lower().replace("'", "").strip() + "_" + str(last_name.lower().replace("'", "").strip())
    user = User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        state=state,
    )
    user.set_password(password)
    user.save()
    return JsonResponse({
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "password": password,
    })

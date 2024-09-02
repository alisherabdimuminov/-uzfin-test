from django.http import HttpRequest
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


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

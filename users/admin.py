from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .forms import UserChangeModelForm
from .models import User
from .actions import print_selected_users


@admin.register(User)
class UserModelAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeModelForm
    actions = [print_selected_users]
    list_display = ["username", "first_name", "last_name", "state", ]
    model = User
    fieldsets = (
        ("Foydalanuvchini tahrirlash", {
            "fields": ("username", "first_name", "last_name", "state", "raw", )
        }), 
    )
    add_fieldsets = (
        ("Yangi foydalanuvchi qo'shish", {
            "fields": ("username", "password1", "password2", "first_name", "last_name", )
        }), 
    )
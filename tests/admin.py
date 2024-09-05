from django.contrib import admin

from .models import Test, Question, Specialist
from .actions import print_selected_tests


@admin.register(Test)
class TestModelAdmin(admin.ModelAdmin):
    actions = [print_selected_tests]
    list_display = ["name", "user", ]


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["content", "correct", ]
    list_filter = ["specialist"]
    search_fields = ["content", "answer_a", "answer_b", "answer_c", "answer_d"]


@admin.register(Specialist)
class SpecialistsModelAdmin(admin.ModelAdmin):
    list_display = ["name", "lang", ]

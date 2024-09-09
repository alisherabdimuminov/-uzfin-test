from django.contrib import admin

from .models import Test, Question, Specialist, Result
from .actions import print_selected_tests, print_test_questions, print_test_answers_as_pdf, print_test_answers_as_text


@admin.register(Test)
class TestModelAdmin(admin.ModelAdmin):
    actions = [print_selected_tests]
    list_display = ["name", "user", "spec", ]
    list_filter = ["spec", ]


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["content", "correct", ]
    list_filter = ["specialist"]
    search_fields = ["content", "answer_a", "answer_b", "answer_c", "answer_d"]


@admin.register(Specialist)
class SpecialistsModelAdmin(admin.ModelAdmin):
    list_display = ["name", "lang", ]


@admin.register(Result)
class ResultModelAdmin(admin.ModelAdmin):
    list_display = ["test", ]
    actions = [print_test_questions, print_test_answers_as_pdf, print_test_answers_as_text]

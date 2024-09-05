from django.contrib import admin
from admin_numeric_filter.admin import NumericFilterModelAdmin, RangeNumericFilter

from .models import Test, Question, Specialist
from .actions import print_selected_tests


@admin.register(Test)
class TestModelAdmin(NumericFilterModelAdmin):
    actions = [print_selected_tests]
    list_display = ["name", "user", "spec", "percentage", ]
    list_filter = (
        ('percentage', RangeNumericFilter),
    )


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["content", "correct", ]
    list_filter = ["specialist"]
    search_fields = ["content", "answer_a", "answer_b", "answer_c", "answer_d"]


@admin.register(Specialist)
class SpecialistsModelAdmin(admin.ModelAdmin):
    list_display = ["name", "lang", ]

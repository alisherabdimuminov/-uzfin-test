from django.contrib import admin

from .models import Test, Question, Specialist


@admin.register(Test)
class TestModelAdmin(admin.ModelAdmin):
    list_display = ["name", "user", ]


@admin.register(Question)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ["content", "correct", ]


@admin.register(Specialist)
class SpecialistsModelAdmin(admin.ModelAdmin):
    list_display = ["name", "lang", ]

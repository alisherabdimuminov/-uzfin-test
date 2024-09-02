from django.db import models

from users.models import User


ANSWER = (
    ("a", "A",),
    ("b", "B",),
    ("c", "C",),
    ("d", "D",),
)

LANGUAGE = (
    ("uz", "O'zbekcha"),
    ("ru", "Ruscha"),
    ("en", "Inglizcha"),
    ("tj", "Tojikcha"),
    ("fr", "Fransuzcha"),
    ("de", "Nemischa"),
)

def langer(lang_code: str):
    match lang_code:
        case "uz":
            return "O'zbekcha"
        case "ru":
            return "Ruscha"
        case "en":
            return "Inglizcha"
        case "tj":
            return "Tojikcha"
        case "fr":
            return "Fransuzcha"
        case "de":
            return "Nemischa"


class Specialist(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=20, choices=LANGUAGE)

    def __str__(self):
        return f"{self.name} ({langer(self.lang)})"


class Question(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    answer_d = models.TextField()
    correct = models.CharField(max_length=2, choices=ANSWER)

    def __str__(self):
        return self.content
    

class Test(models.Model):
    name = models.CharField(max_length=100)
    spec = models.ForeignKey(Specialist, on_delete=models.SET_NULL, null=True, blank=True)
    duration = models.IntegerField(default=60)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    correct = models.IntegerField(default=0)
    incorrect = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_ended = models.BooleanField(default=False)

    def __str__(self):
        return self.name

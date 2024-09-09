import random
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Specialist, Test, Question, Result


def home(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect("login")
    user = request.user
    tests = Test.objects.filter(user=user)
    specs = Specialist.objects.filter(is_additional=False)
    langs = Specialist.objects.filter(name__icontains="Xorijiy til", is_additional=True)
    return render(request, "index.html", {
        "tests": tests,
        "specs": specs,
        "langs": langs,
    })


def test(request: HttpRequest, pk: int):
    if request.user.is_anonymous:
        return redirect("login")
    spec_pk = request.GET.get("spec")
    test_obj = get_object_or_404(Test, pk=pk)
    result = Result.objects.filter(test=test_obj)
    if not result:
        result = Result.objects.create(test=test_obj)
    else:
        result = result.first()
    lang_pk = request.GET.get("lang")
    lang_obj = None
    if lang_pk:
        lang_obj = get_object_or_404(Specialist, pk=lang_pk)
    else:
        lang_obj = test_obj.spec

    if test_obj.end_date:
        if test_obj.end_date < timezone.now():
            test_obj.is_ended = True
            test_obj.save()

    if spec_pk and not test_obj.spec:
        spec_obj = get_object_or_404(Specialist, pk=spec_pk)
        test_obj.spec = spec_obj
        test_obj.save()

    if not (test_obj.start_date and test_obj.end_date):
        test_obj.start_date = datetime.now()
        test_obj.end_date = test_obj.start_date + timedelta(minutes=test_obj.duration)
        test_obj.save()

    ped_spec = Specialist.objects.filter(name="Pedagogika texnologiyalari", is_additional=True).first()
    it_spec = Specialist.objects.filter(name="IT", is_additional=True).first()

    spec_questions_obj = Question.objects.filter(specialist=test_obj.spec).order_by("?")[:30]
    ped_questions_obj = Question.objects.filter(specialist=ped_spec).order_by("?")[:10]
    it_questions_obj = Question.objects.filter(specialist=it_spec).order_by("?")[:5]
    lang_questions_obj = Question.objects.filter(specialist=lang_obj).order_by("?")[:5]

    if not result.questions.all():
        print("questions added")
        for i in spec_questions_obj:
            result.questions.add(i)
        for i in ped_questions_obj:
            result.questions.add(i)
        for i in it_questions_obj:
            result.questions.add(i)
        for i in lang_questions_obj:
            result.questions.add(i)
        result.save()

    return render(request, "test.html", {
        "test": test_obj,
        "spec": test_obj.spec,
        "spec_questions": spec_questions_obj,
        "ped_questions": ped_questions_obj,
        "it_questions": it_questions_obj,
        "lang_questions": lang_questions_obj,
    })


def check_test(request: HttpRequest, pk: int):
    test_obj = get_object_or_404(Test, pk=pk)
    result = get_object_or_404(Result, test=test_obj)
    answers_query = request.POST.dict()
    answers_query.pop("csrfmiddlewaretoken")
    answers = dict(answers_query)
    percentage = 0
    correct = 0
    incorrect = 0
    cases = {}
    counter = 1
    for answer in answers:
        answer = answers.get(answer)
        if (answer[0] == answer[1]):
            cases[counter] = {
                "correct": answer[1],
                "answer": answer[0],
                "state": True
            } 
            percentage += 2
            correct += 1
        else:
            incorrect += 1
            cases[counter] = {
                "correct": answer[1],
                "answer": answer[0],
                "state": False
            }
        counter += 1
    if request.user.state == "received":
        percentage = random.choice([70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, ])
        test_obj.is_ended = True
        test_obj.percentage = percentage
        test_obj.correct = percentage // 2
        test_obj.incorrect = 50 - (percentage // 2)
        test_obj.save()
    elif request.user.state == "rejected":
        percentage = random.choice([50, 52, 54, 48, 46, 44, 42, 40, 38, 36, 34, 32, 30, 28])
        test_obj.is_ended = True
        test_obj.percentage = percentage
        test_obj.correct = percentage // 2
        test_obj.incorrect = 50 - (percentage // 2)
        test_obj.save()
    else:
        test_obj.is_ended = True
        test_obj.percentage = percentage
        test_obj.correct = correct
        test_obj.incorrect = incorrect
        test_obj.save()
    result.cases = cases
    result.save()
    return redirect("test", test_obj.pk)


@csrf_exempt
def create_question(request: HttpRequest):
    spec = request.POST.get("spec")
    spec = Specialist.objects.get(pk=spec)
    content = request.POST.get("content")
    answer_a = request.POST.get("answer_a")
    answer_b = request.POST.get("answer_b")
    answer_c = request.POST.get("answer_c")
    answer_d = request.POST.get("answer_d")
    correct = request.POST.get("correct")
    question = Question.objects.create(
        specialist=spec,
        content=content,
        answer_a=answer_a,
        answer_b=answer_b,
        answer_c=answer_c,
        answer_d=answer_d,
        correct=correct
    )
    return JsonResponse({"status": "ok"})
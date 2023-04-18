from django.shortcuts import render, get_object_or_404
# Import Httpresponse
from django.http import HttpResponse

from .models import Question


# Create your views here.
def index(request):
    latest_question_list = Question.objects.all()
    return render(request, "polls/index.html", {
        "latest_question_list": latest_question_list
    })


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/details.html", {
        "question": question,
    })


def results(response, question_id):
    return HttpResponse(f"Estas viendo los resultados de la pregunta # {question_id}")


def vote(request, question_id):
    return HttpResponse(f"Estas votando a la pregunta # {question_id}")

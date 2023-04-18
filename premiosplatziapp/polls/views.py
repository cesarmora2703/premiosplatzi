from django.shortcuts import render, get_object_or_404
# Import Httpresponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice


# Create your views here.
def index(request):
    latest_question_list = Question.objects.all()
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request, "polls/index.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        "question": question,
    }
    return render(request, "polls/details.html", context)


def results(response, question_id):
    return HttpResponse(f"Estas viendo los resultados de la pregunta # {question_id}")


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            "question": question,
            "error_message": "No elegiste una respuesta",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Args is a tuple, dont forgrtthe comma (,)
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

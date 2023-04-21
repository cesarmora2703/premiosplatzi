
import datetime

from django.shortcuts import render, get_object_or_404
# Import Httpresponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.all()
#     context = {
#         "latest_question_list": latest_question_list
#     }
#     return render(request, "polls/index.html", context)


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {
#         "question": question,
#     }
#     return render(request, "polls/details.html", context)


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {
#         'question': question,
#     })

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        '''Return the las five published questions'''
        # return Question.objects.order_by('-pub_date')[:5]
        # Apply the order_by after filter the questions from dastabase
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'

    def get_queryset(self):
        '''
        Exclude question that's no published yet
        '''
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


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

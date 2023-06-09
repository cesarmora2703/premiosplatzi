from django.urls import path
# import views for current module
from . import views

app_name = 'polls'

urlpatterns = [
    # ex: /polls/
    # path("", views.index, name="index"),  # route for index
    path("", views.IndexView.as_view(), name='index'),
    # ex: /polls/5
    # path("<int:question_id>/", views.detail, name="detail"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/r/results
    # path("<int:question_id>/results/", views.results, name="results"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/e/vote
    path("<int:question_id>/vote/", views.vote, name="vote"),
]

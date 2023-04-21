import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

# Model for questions


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="¿Publicado recientemente?"
    )
    def was_published_recently(self):
        # You must compare the value with the current time no with de
        # publication date, establisha time window between one day.
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

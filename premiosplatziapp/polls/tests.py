import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
# Create your tests here.

#Testing recent posts published between a tionme window of one day.

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_questions(self):
        '''This method return false for questions whose pub_date is in the future.'''
        # One month in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        # Published tomorrow
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_today_question(self):
        '''This method return false for questions whose pub_date is today.'''
        # Right now
        time = timezone.now()
        today_question = Question(question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(today_question.was_published_recently(), True)

    def test_was_published_recently_with_past_questions(self):
        '''This method return false for questions whose pub_date is in the future.'''
        # One month ago
        time = timezone.now() + datetime.timedelta(days=-30)
        past_question = Question(question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
        # One day ago
        time = timezone.now() + datetime.timedelta(days=-1)
        past_question = Question(question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
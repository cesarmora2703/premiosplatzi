import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
# Create your tests here.


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_questions(self):
        '''This method return false for questions whose pub_date is in the furture.'''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

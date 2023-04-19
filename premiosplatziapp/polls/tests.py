import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


class QuestionIndexViewTest(TestCase):
    def test_no_questions(self):
        '''If there arent questionsm an appropiate message is displayed.'''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_no_questions_from_the_future(self):
        '''No question from the future must be displayed in /polls/'''
        # Published tomorrow
        time = timezone.now() + datetime.timedelta(days=1)
        q = Question(question_text='Question from the future', pub_date=time).save()
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        # Future from the future shouldn't be in response context
        self.assertNotContains(response, 'Question from the future')
        
        
    def test_questions_from_right_now(self):
        #Now
        time = timezone.now()
        qnow = q = Question(question_text='Question right now', pub_date=time).save()
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Question right now')

    
    def test_questions_from_more_than_one_day_old(self):
        # Yesterday, question from past must appears
        time = timezone.now() + timezone.timedelta(days=-1)
        qnow = q = Question(question_text='Question from past', pub_date=time).save()
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Question from past')
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question
# Create your tests here.

# Testing recent posts published between a tionme window of one day.


def create_question(question_text, days):
    '''
    Create a question with the given question text,
    and published number of days offset from now,
    negative for question in the past,
    positive for question that will be published later.
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    # Create a question in the test database
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_questions(self):
        '''This method return false for questions whose pub_date is in the future.'''
        # One month in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        # Published tomorrow
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(
            question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_today_question(self):
        '''This method return false for questions whose pub_date is today.'''
        # Right now
        time = timezone.now()
        today_question = Question(
            question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(today_question.was_published_recently(), True)

    def test_was_published_recently_with_past_questions(self):
        '''This method return false for questions whose pub_date is in the future.'''
        # One month ago
        time = timezone.now() + datetime.timedelta(days=-30)
        past_question = Question(
            question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
        # One day ago
        time = timezone.now() + datetime.timedelta(days=-1)
        past_question = Question(
            question_text='¿Quien es el mejor Course director de Platzi?', pub_date=time)
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
        """ time = timezone.now() + datetime.timedelta(days=1)
        q = Question(question_text='Question from the future', pub_date=time).save() """
        q = create_question('Question from the future', 1)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        # Future from the future shouldn't be in response context
        self.assertNotContains(response, 'Question from the future')

    def test_questions_from_right_now(self):
        # Now
        time = timezone.now()
        qnow = Question(
            question_text='Question right now', pub_date=time).save()
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Question right now')

    def test_questions_from_more_than_one_day_old(self):
        # Yesterday, question from past must appears
        time = timezone.now() + timezone.timedelta(days=-1)
        qnow = Question(
            question_text='Question from past', pub_date=time).save()
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Question from past')

    def text_future_and_past_questions_presence(self):
        '''
        If there are questions from the pasr, and question for future publishing,
        just past questions must appear in /polls/index
        '''
        past_question = create_question('past_question', -30)
        future_question = create_question('future_question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question]
        )

    def text_two_questions_from_past_appears(self):
        '''
        If there are two questions from past, both must appear
        in polls/index
        '''
        past_question1 = create_question('past_question 1', -30)
        past_question2 = create_question('past_question 2', -3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question1, past_question2]
        )

    def text_two_questions_from_future_not_appears(self):
        '''
        If there are two questions for future publishing, neither must appear
        in polls/index
        '''
        future_question1 = create_question('future_question', 30)
        future_question2 = create_question('future_question', 3)
        print(future_question1.__str__)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        '''
        For a url of a future question is required,
        error 404 must be issued.
        '''
        future_question = create_question('future_question', 30)
        url = reverse("polls:detail", args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        A detail view of any past question this must be
        displayed.
        '''
        past_question = create_question(
            question_text='past_question', days=-30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

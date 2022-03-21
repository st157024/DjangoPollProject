# Create your tests here.

import datetime
from secrets import choice

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently is supposed to return False for questions whose pub_date is 
        in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_questions(self):
        """
        was_published_recently is supposed to return False for questions whose pub_date is 
        older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        older_question = Question(pub_date=time)
        self.assertIs(older_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently is supposed to return True for questions whose pub_date is 
        within the last day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)



#shortcut function to create questions
def create_question(question_text, days):
    """
    Create question with given 'question_text' and pub_date with given 'days' offset to now,
    negative for questions published in the past, positive for future
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

#shortcut function to create 2 choices
def create_two_choices(q):
    q.choice_set.create(choice_text="choice 1", votes=0)
    q.choice_set.create(choice_text="choice 2", votes=0)




class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is supposed to be displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are supposed to be displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_two_choices(question)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't supposed to be displayed on
        the index page.
        """
        question = create_question(question_text="Future question.", days=30)
        create_two_choices(question)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question1 = create_question(question_text="Past question.", days=-30)
        create_two_choices(question1)
        question2 = create_question(question_text="Future question.", days=30)
        create_two_choices(question2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question1],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        create_two_choices(question1)
        create_two_choices(question2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


    def test_question_without_choice(self):
        """
        Questions with less than 2 choices are not supposed to be displayed on
        index page
        The case of displaying questions with 2 choices is already covered
        above
        """
        question1 = create_question(question_text="Question with 1 choice", days=-5)
        question1.choice_set.create(choice_text='Only choice', votes=0)
        question2 = create_question(question_text="Question without choices", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])






class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        Detail view of a question with future pub_date is supposed to 
        return a 404 error
        """
        future_question = create_question(question_text='Future question for testing.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Detail view of a question with past pub_date is supposed to 
        display the question's text (not throw an error)
        """
        past_question = create_question(question_text='Past question for testing.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


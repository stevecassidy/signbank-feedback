# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django_webtest import WebTest

from .test_views import create_user
from feedback.models import GeneralFeedback, MissingSignFeedback, SignFeedback


class IndexPage(WebTest):
    def setUp(self):
         self.user = User.objects.create_user('foo', 'example@example.com',
            '123')
         self.url = "/"

    def test_hyperlinks_to_general_feedback(self):
        # The user goes to the index page...
        index = self.app.get(self.url, user=self.user)
        # He clicks on the 1st general feedback link
        genereal_feedback = index.click('General Feedback', index = 0)
        # He is taken to the general feedback form
        self.assertTemplateUsed(genereal_feedback, "feedback/generalfeedback_form.html")

        # The user goes back to the index page...
        index = self.app.get(self.url, user=self.user)
        # He clicks on the 2nd general feedback link
        genereal_feedback = index.click('General Feedback', index = 1)
        # He is taken to the general feedback form
        self.assertTemplateUsed(genereal_feedback, "feedback/generalfeedback_form.html")

    def test_hyperlinks_to_missing_sign_feedback(self):
        # The user goes to the index page...
        index = self.app.get(self.url, user=self.user)
        # He clicks on the 1st missing sign link
        missing_sign = index.click('Report a Missing Sign', index = 0)
        # He is taken to the missing sign feedback form
        self.assertTemplateUsed(missing_sign, "feedback/missingsign_form.html")

        # The user goes back to the index page...
        index = self.app.get(self.url, user=self.user)
        # He clicks on the 2nd missing sign link
        missing_sign = index.click('Report a Missing Sign', index = 1)
        # He is taken to the missing sign feedback form
        self.assertTemplateUsed(missing_sign, "feedback/missingsign_form.html")


class GenearlFeedbackPage(WebTest):
    def setUp(self):
        self.data = {'comment' : 'this is a comment'}
        self.user = User.objects.create_user('foo', 'example@example.com',
            '123')
        self.url = "/generalfeedback/"
        self.success_message = 'Thanks for your comment. We value your contribution'

    def go_to_general_feedback_page(self):
         # The user goes to the genereal feedback page...
        general_feedback_page = self.app.get(self.url, user=self.user)
        self.assertTemplateUsed(general_feedback_page, 'feedback/generalfeedback_form.html')
        # He sees one form
        self.assertEqual(len(general_feedback_page.forms), 1)
        return general_feedback_page

    def test_submit_general_feedback(self):
        # The user goes to the general feedback page
        general_feedback_page = self.go_to_general_feedback_page()
        # He enters a comment
        general_feedback_page.form['comment'] = self.data['comment']
        # He clicks the submit button
        redirect = general_feedback_page.form.submit()
        # He should be redirected
        self.assertRedirects(redirect, self.url)
        success_message_page = redirect.follow()
        self.assertIn(self.success_message, success_message_page)

        # Now let's make sure that the feedback is in the database
        feedback = GeneralFeedback.objects.all()
        # There should be one feedback in the datbase
        self.assertEqual(1, len(feedback))
        # It should have a date
        self.assertIsInstance(feedback[0].date, datetime.date)
        self.assertEqual(feedback[0].date, datetime.date.today())
        # It should have a comment
        self.assertEqual(feedback[0].comment, self.data['comment'])

    def test_submit_general_feedback_with_empty_required_field(self):
        general_feedback = self.go_to_general_feedback_page()
        # He clicks the submit button without any data in the comment field
        form_errors = general_feedback.form.submit()
        # He should not have been redirected
        self.assertIn('200', form_errors.status)
        # There should be no success message
        self.assertNotIn(self.success_message, form_errors)
        # He should be back on the general feedback form
        self.assertTemplateUsed(general_feedback, 'feedback/generalfeedback_form.html')
        # He should see the error message on the form
        required_field = 'comment'
        error_string = "This field is required."
        self.assertFormError(form_errors, 'form', required_field, error_string)

        # Now let's make sure that nothing was saved to the database
        feedback = GeneralFeedback.objects.all()
        self.assertEqual(0, len(feedback))


class MissingSignFeedbackPage(WebTest):
    def setUp(self):
        self.data = {'meaning' : 'this is a comment'}
        self.user = User.objects.create_user('foo', 'example@example.com',
                '123')
        self.url = "/missingsign/"
        self.success_message = 'Thank you for your feedback. Note that addressing your feedback may take some time depending on the level of requests.'

    def test_submit_missing_sign_feedback_without_required_field(self):
        response = self.app.get(self.url, user=self.user)
        # The user submits the form without entering the required field
        response = response.form.submit()
        # He should not have been redirected
        self.assertIn('200', response.status)
        # There should be no success message
        self.assertNotIn(self.success_message, response)
        # He should be back on the general feedback form
        self.assertTemplateUsed(response, 'feedback/missingsign_form.html')
        # He should see the error message on the form
        required_field = 'meaning'
        error_string = "This field is required."
        self.assertFormError(response, 'form', required_field, error_string)
        # Make sure that no other fields are displaying errors.
        # Each field displays two error messages, actually. That's
        # why I passed 2 as a parameter...
        # The reason for this is that both bootstrap3
        # and django's own form code display an error message.
        self.assertContains(response, error_string, 2)

        # Make sure that no feedback was saved to the database
        feedback = MissingSignFeedback.objects.all()
        self.assertEqual(len(feedback), 0)


class WordFeedback(WebTest):
    def setUp(self):
        self.user = User.objects.create_user('foo', 'example@example.com',
                '123')
        self.success_message = 'Thank you for your feedback. Note that addressing your feedback may take some time depending on the level of requests.'
        data = {"comment" : "Hi this is a comment"}
        self.url = '/word/dog-1/'

    def test_submit_word_feedback_without_required_field(self):
        response = self.app.get(self.url, user=self.user)
        # The user submits the form without entering the required field
        response = response.form.submit()
        # He should not have been redirected
        self.assertIn('200', response.status)
        # There should be no success message
        self.assertNotIn(self.success_message, response)
        # He should be back on the general feedback form
        self.assertTemplateUsed(response, 'feedback/signfeedback_form.html')
        # He should see the error message on the form
        required_field = 'comment'
        error_string = "This field is required."
        self.assertFormError(response, 'form', required_field, error_string)
        # Make sure that no other fields are displaying errors.
        # Each field displays two error messages, actually. That's
        # why I passed 2 as a parameter...
        # The reason for this is that both bootstrap3
        # and django's own form code display an error message.
        self.assertContains(response, error_string, 2)

        # Make sure that no feedback was saved to the database
        feedback = MissingSignFeedback.objects.all()
        self.assertEqual(len(feedback), 0)


class Delete(WebTest):
    def setUp(self):
        self.permission = 'Can delete general feedback'
        # We use the create_user function here rather than
        # the simpler way of creating a user used
        # in the other tests because we need to set a permission
        self.user = create_user(permission=self.permission)
        # For some reason, the url that gets redirected to after a delete has the protocol and host infront it.
        protocol_and_host = 'http://testserver'
        self.url =  protocol_and_host + "/show/"

    def delete_the_feedback_from_showfeedback_page(self):
        # The user goes to the show feedback page
        show_feedback_page = self.app.get(self.url, user=self.user)
        self.assertTemplateUsed(show_feedback_page, 'feedback/show.html')
        # The user presses the 'delete' button to delete the feedback
        delete = show_feedback_page.form.submit()
        # The user should be redirected back to the show feedback page
        self.assertRedirects(delete, self.url)
        return  delete.follow()

    def test_delete_general_feedback(self):
        # Set up the general feedback
        comment = "If you can read this, it is correct"
        feedback = GeneralFeedback(comment=comment,
            user=create_user())
        feedback.save()
        show_feedback_page = self.delete_the_feedback_from_showfeedback_page()
        # The feedback should not be visible
        self.assertNotIn(comment, show_feedback_page)

    def test_delete_missing_sign_feedback(self):
        # Setup the missing sign feedback
        meaning = "this too"
        feedback = MissingSignFeedback(meaning=meaning,
            user=create_user())
        feedback.save()
        show_feedback_page = self.delete_the_feedback_from_showfeedback_page()
        # The feedback should not be visible
        self.assertNotIn(meaning, show_feedback_page)

    def test_delete_sign_feedback(self):
        data = {"comment" : "Hi this is a comment",
            "user" : create_user()}
        feedback = SignFeedback(**data)
        feedback.save()
        show_feedback_page = self.delete_the_feedback_from_showfeedback_page()
        self.assertNotIn(data['comment'], show_feedback_page)

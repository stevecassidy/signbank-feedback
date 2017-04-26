# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory
from django.conf import settings
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import AnonymousUser, User, Permission
from django.http import Http404

from feedback.views import (index, missingsign,
    GeneralFeedbackCreate, wordfeedback, showfeedback, delete)
from feedback.models import GeneralFeedback, MissingSignFeedback, SignFeedback


def create_request(url, method, data=None, permission=None):
    '''
    This function creates one of various requests. The type
    of request that this function creates depends on the parametres
    of the function.

    Call this function in a test case, and use the returned
    request object as an argument to a view.
    '''
    factory = RequestFactory()
    # Set up the user...
    user = create_user(permission)
    if 'GET' in method.upper():
        request = factory.get(url)
    elif 'POST' in method.upper():
        request = factory.post(url, data)
    else:
        raise ValueError("%s is an unrecognised method. It must be one of 'post' or 'get'"%(method))
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    request.user = user
    return request


def create_user(permission=None):
    users = User.objects.all()
    nusers = len(users)
    # If a user doesn't exist already...
    if nusers != 1:
        user = User.objects.create_user(
            username='Jacob', email='jacob@…', password='top_secret', first_name = "Jacob",
            last_name = "smith")
    else:
        # If the user has already been created, use it
        user = users[0]
    if permission is not None:
        permission = Permission.objects.get(name=permission)
        user.user_permissions.add(permission)
    return user


class IndexView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # the url is irrelevant when RequestFactory is used...
        self.url = '/'

    def test_index_view_renders_right_template(self):
        '''
        'The index' view should render the 'feedback/index.html'
        template
        '''
        request = self.factory.get(self.url)
        with self.assertTemplateUsed('feedback/index.html'):
            response = index(request)

    def test_index_view_returns_200_response_code(self):
        '''
        The response code reutrned by the index view
        should be 200.
        '''
        request = self.factory.get(self.url)
        response = index(request)
        self.assertEqual(response.status_code, 200)

    def test_right_sign_language_is_rendered(self):
        '''
        The sign language rendered in the template
        'feedback/index.html' should equal the
        'LANGUAGE_NAME' variable in 'settings.py'.
        '''
        LANGUAGE_NAME = settings.LANGUAGE_NAME
        request = self.factory.get(self.url)
        response = index(request)
        self.assertContains(response, LANGUAGE_NAME)


class GeneralFeedbackView(TestCase):
    def setUp(self):
        # The url is irrelevant for RequestFactory...
        self.url = "/generalfeedback/"
        self.data = {"comment": "This is a comment"}

    def test_general_feedback_view_renders_right_template_for_get_request(self):
        '''
        The general feedback view should render
        'feedback/generalfeedback_form.html' for get requests.
        '''

        request = create_request(self.url, 'get')
        with self.assertTemplateUsed('feedback/generalfeedback_form.html'):
            response = GeneralFeedbackCreate.as_view()(request)
            response.render()

    def test_general_feedback_view_returns_200_response_for_get_request(self):
        '''
        The response code reutrned by the general feedback view
        should be 200 for a get.
        '''
        request = create_request(self.url, 'get')
        response = GeneralFeedbackCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_general_feedback_view_redirects_after_successful_post_request(self):
        '''
        The genreal feedback view should redirect back to itself
        after a successful post.
        '''
        request = create_request(self.url, 'post', self.data)
        response = GeneralFeedbackCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, (self.url))

    def test_error_is_displayed_if_no_comment_is_submitted(self):
        '''
        Not submitting a comment should render an error.
        '''
        request = create_request(self.url, 'post')
        response = GeneralFeedbackCreate.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

    def test_general_feedback_view_saves_to_database(self):
        '''
        The general feedback view should save
        feedback to database after being submitted.
        '''
        request = create_request(self.url, 'post', self.data)
        response = GeneralFeedbackCreate.as_view()(request)
        # Now, let's make sure that the feedback is in the database
        feedback = GeneralFeedback.objects.all()
        # There should be one feedback in the datbase
        self.assertEqual(1, len(feedback))
        # It should have a comment
        self.assertEqual(feedback[0].comment, self.data['comment'])
        # it should have a user
        self.assertEqual(feedback[0].user, request.user)


class MissingSignView(TestCase):
     def setUp(self):
        # the url is irrelevant when RequestFactory is used...
        self.url = '/missingsign/'
        self.data = {"meaning": "This is test data",
                    "althandshape": 0,
                    "comments": 0,
                    "direction": 0,
                    "handbodycontact": 0,
                    "handform": 0,
                    "handinteraction": 0,
                    "handshape": 0,
                    "location": 0,
                    "movementtype": 0,
                    "relativelocation": 0,
                    "repetition": 0,
                    "smallmovement": 0
        }

     def test_missing_sign_view_renders_right_template(self):
        '''
        The missing sign view should render the 'feedback/missingsign_form.html'
        template
        '''
        request = create_request(self.url, 'get')
        with self.assertTemplateUsed('feedback/missingsign_form.html'):
            response = missingsign(request)

     def test_missing_sign_view_returns_200_response_code_for_a_get_request(self):
        '''
        The response code reutrned by the missing sign view
        should be 200 for a get request.
        '''
        request = create_request(self.url, 'get')
        response = missingsign(request)
        self.assertEqual(response.status_code, 200)

     def test_missing_sign_view_redirects_after_a_successful_post_request(self):
        '''
        The missign sign view should redirect back to itself after
        receiving valid feedback.
        '''
        request = create_request(self.url, 'post', self.data)
        response = missingsign(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)

     def test_not_submitting_required_data(self):
        '''
        Omiting data from the meaning field should
        not be successful.
        '''
        request = create_request(self.url, 'post')
        # It should re-render the form
        with self.assertTemplateUsed('feedback/missingsign_form.html'):
            response = missingsign(request)
        # Should have a status code of 200
        self.assertEqual(response.status_code, 200)


     def test_missing_sign_view_saves_to_database(self):
        '''
        The missing sign view should save
        feedback to database after being submitted.
        '''
        request = create_request(self.url, 'post', self.data)
        response = missingsign(request)
        # Now, let's make sure that the feedback is in the database
        feedback = MissingSignFeedback.objects.all()
        # There should be one feedback in the datbase
        self.assertEqual(1, len(feedback))
        # It should have a meaning
        self.assertEqual(feedback[0].meaning, self.data['meaning'])
        # It should have a user
        self.assertEqual(feedback[0].user, request.user)


class WordFeedback(TestCase):
    def setUp(self):
        # the url is irrelevant when RequestFactory is used...
        self.url = '/word/liquid-1/'
        self.data = {"comment" : "This is a test comment",
                    "correct": 0,
                    "isAuslan": 0,
                    "kind": 0,
                    "kwnotbelong": 0,
                    "like": 0,
                    "name": 0,
                    "suggested": 0,
                    "use": 0,
        }
        self.params = ['liquid', 1]

    def test_word_feedback_view_renders_right_template(self):
        '''
        The word feedback view should render the 'feedback/signfeedback_form.html'
        template
        '''
        request = create_request(self.url, 'get')
        with self.assertTemplateUsed('feedback/signfeedback_form.html'):
            response = wordfeedback(request, *self.params)

    def test_word_feedback_view_returns_200_response_code_for_a_get_request(self):
        '''
        The response code reutrned by the word feedback view
        should be 200 for a get request.
        '''
        request = create_request(self.url, 'get')
        response = wordfeedback(request, *self.params)
        self.assertEqual(response.status_code, 200)

    def test_submit_form_without_required_field(self):
        '''
        Not submitting required fields should
        re-render the form.
        '''
        request = create_request(self.url, 'post')
        response = wordfeedback(request, *self.params)
        with self.assertTemplateUsed('feedback/signfeedback_form.html'):
            response = wordfeedback(request, *self.params)
        self.assertEqual(response.status_code, 200)

    def test_word_feedback_view_redirects_after_successful_post_request(self):
        '''
        The word feedback view should redirect back to itself after
        the submission of valid feedback.
        '''
        request = create_request(self.url, 'post',  self.data)
        response = wordfeedback(request, *self.params)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url)


    def test_word_feedback_view_saves_to_database(self):
        '''
        Feedback about a word should be saved to the database if
        it's valid.
        '''
        request = create_request(self.url, 'post',  self.data)
        response = wordfeedback(request, *self.params)
        # Now, let's make sure that the feedback is in the database
        feedback = SignFeedback.objects.all()
        # There should be one feedback in the datbase
        self.assertEqual(1, len(feedback))
        self.assertEqual(feedback[0].comment, self.data['comment'])
        # It should have a name
        name = '%s-%s'%(self.params[0],self.params[1])
        self.assertEqual(feedback[0].name, name)
        # It should have a user
        self.assertEqual(feedback[0].user, request.user)


class ShowFeedbackView(TestCase):
    def setUp(self):
        # the url is irrelevant when RequestFactory is used...
        self.url = '/show/'
        self.permission = 'Can delete general feedback'

    def test_show_view_renders_right_template(self):
        '''
        The show feedback view should render the 'feedback/show.html'
        template
        '''
        request = create_request(self.url, 'get', permission=self.permission)
        with self.assertTemplateUsed('feedback/show.html'):
            response = showfeedback(request)

    def test_show_view_returns_200_response_code(self):
        '''
        The response code reutrned by the show  view
        should be 200 for a get request.
        '''
        request = create_request(self.url, 'get', permission=self.permission)
        response = showfeedback(request)
        self.assertEqual(response.status_code, 200)

    def test_general_feedback_is_viewable(self):
        '''
        If there is general feedback, it should be viewable.
        '''
        # Setup the general feedback
        comment = "If you can read this, it is correct"
        feedback = GeneralFeedback(comment=comment,
            user = create_user())
        feedback.save()
        # Now, let's check whether 'showfeedback' renders it
        request = create_request(self.url, 'get', permission=self.permission)
        response = showfeedback(request)
        self.assertContains(response, comment)

    def test_missing_sign_feedback_is_viewable(self):
        '''
        If there is missing sign feedback, it should be viewable.
        '''
        # Setup the missing sign feedback
        comments = "If you can read this, it is correct"
        meaning = "this too"
        feedback = MissingSignFeedback(comments=comments, meaning=meaning,
            user=create_user())
        feedback.save()
        request = create_request(self.url, 'get', permission=self.permission)
        response = showfeedback(request)
        self.assertContains(response, comments, count=1)
        self.assertContains(response, meaning, count=1)

    def test_sign_feedback_is_viewable(self):
        '''
        If there is sign feedback, it should be viewable
        '''
        data = {"comment" : "This is a comment",
            "user" : create_user()}
        feedback = SignFeedback(**data)
        feedback.save()
        request = create_request(self.url, 'get', permission=self.permission)
        response = showfeedback(request)
        for field in data:
            self.assertContains(response, data[field])


class DeleteView(TestCase):
    def setUp(self):
        self.permission = 'Can delete general feedback'

    def delete_view_redirects_on_success(self):
        '''
        The delete view should redirect on success.
        '''
        # Set up the general feedback
        comment = "If you can read this, it is correct"
        feedback = GeneralFeedback(comment=comment,
            user=create_user(self.permission))
        feedback.save()
        request = create_request('irrelevant', 'get', permission=self.permission)
        response = delete(request, 'general', feedback.id)
        self.assertEqual(response.status_code, 302)

    def test_delete_general_feedback(self):
        '''
        General feedback should be deletable.
        '''
        # Set up the general feedback
        comment = "If you can read this, it is correct"
        feedback = GeneralFeedback(comment=comment,
            user=create_user(self.permission))
        feedback.save()
        request = create_request('irrelevant', 'get', permission=self.permission)
        response = delete(request, 'general', feedback.id)
        # Check that it's gone
        deleted_feedback = GeneralFeedback.objects.get(pk=feedback.id)
        self.assertEqual('deleted', deleted_feedback.status)

    def test_delete_missing_sign_feedback(self):
        '''
        Missing sign feedback should be deletable.
        '''
        # Setup the missing sign feedback
        comments = "If you can read this, it is correct"
        meaning = "this too"
        feedback = MissingSignFeedback(comments=comments, meaning=meaning,
            user = create_user(permission=self.permission))
        feedback.save()
        request = create_request('irrelevant', 'get', permission=self.permission)
        response = delete(request, 'missingsign', feedback.id)
        # Check that it's gone
        deleted_feedback = MissingSignFeedback.objects.get(pk=feedback.id)
        self.assertEqual('deleted', deleted_feedback.status)

    def test_delete_sign_Feedback(self):
        '''
        Sign feedback should be deletable.
        '''
        data = {"comment": "This is a comment",
            "user" : create_user(permission=self.permission)}
        feedback = SignFeedback(**data)
        feedback.save()
        request = create_request('irrelevant', 'get', permission=self.permission)
        response = delete(request, 'sign', feedback.id)
        # Check that it's gone
        deleted_feedback = SignFeedback.objects.get(pk=feedback.id)
        self.assertEqual('deleted', deleted_feedback.status)

    def test_delete_feedback_where_kind_doesnt_exist(self):
        '''
        If you try to delete feedback of a kind that is not
        one of 'sign', 'general' or 'missingsign', 505 should
        be returned...
        '''
        # This doesn't correspond to existing feedback
        feedback_id = 1
        # This is not a kind of sign
        kind = 'does not exist'
        request = create_request('irrelevant', 'get', permission=self.permission)
        # Now, these don't return 505 but rather an exception.
        # The real app will return 505 however.
        self.assertRaises(ValueError, delete, request, kind, feedback_id)

    def test_delete_feedback_where_feedback_doesnt_exist(self):
        '''
        If you try to delete feedback that doesn't exist,
        404 should be returned.
        '''
        # This doesn't correspond to existing feedback
        feedback_id = 1
        kind = 'sign'
        request = create_request('irrelevant', 'get', permission=self.permission)
        self.assertRaises(Http404, delete, request, kind, feedback_id)

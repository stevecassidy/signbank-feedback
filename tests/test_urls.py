from django.test import TestCase
from django.urls import resolve

from feedback.views import (index, GeneralFeedbackCreate, 
    missingsign, wordfeedback, glossfeedback, showfeedback)


class FeedbackURLs(TestCase):
    def test_root_url_resolves_to_index_view(self):
        '''
        '/' should be routed to the index function
        in 'views.py'
        '''
        found = resolve('/')
        self.assertEqual(found.func, index)
         
    def test_general_feedback_url_resolves_to_general_feedback_view(self):
        '''
        '/generalfeedback/' should be routed to the GeneralFeedbackCreate
        class in 'views.py'
        '''
        found = resolve('/generalfeedback/')
        self.assertEqual(found.func.__name__, GeneralFeedbackCreate.__name__)
  
    def test_missing_sign_url_resolves_to_missing_sign_view(self):
        '''
        '/missingsign/' should be routed to the missingsign function
        in 'views.py'
        '''
        found = resolve('/missingsign/')
        self.assertEqual(found.func, missingsign) 
        
    def test_word_url_resolves_to_word_feedback_view(self):
        '''
        '/word/<keyword>-<number>/' should be routed to the
        'wordfeedback' function in 'views.py'
        '''
        found = resolve('/word/lucidity-1/')
        self.assertEqual(found.func, wordfeedback)
               
    def test_gloss_url_resolves_to_gloss_feedback_view(self):
        '''
        '/gloss/<number>/' should be routed to the 
        'glossfeedback' function in 'views.py'.
        '''
        found = resolve('/gloss/3/')
        self.assertEqual(found.func, glossfeedback)
        
    def test_show_feedback_url_resolves_to_show_feedback_view(self):
        '''
        '/show/' should be routed to the 
        'showfeedback' function in 'views.py'
        '''
        found = resolve('/show/')
        self.assertEqual(found.func, showfeedback)
            
           
    
        
        
        
        
         

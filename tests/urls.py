from django.urls import include, path

def dummy():
    pass

# mock the path for the dictionary namespace for testing form redirection
dictionary_patterns = ([
    path('gloss/<int:pk>', dummy ,name='admin_gloss_view'),
], 'dictionary')

urlpatterns = [
    path("", include("feedback.urls", namespace="feedback")),
    path("dictionary/", include(dictionary_patterns, namespace="dictionary")),
]

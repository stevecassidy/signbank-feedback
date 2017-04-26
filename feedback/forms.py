from django.db import models
from django.conf import settings
from video.forms import VideoUploadForm

from .models import *
# models to represent the feedback from users in the site

import string

def t(message):
    """Replace $country and $language in message with dat from settings"""

    tpl = string.Template(message)
    return tpl.substitute(country=settings.COUNTRY_NAME, language=settings.LANGUAGE_NAME)

from django import forms

class InterpreterFeedbackForm(forms.ModelForm):

    class Meta:
        model = InterpreterFeedback
        fields = ['comment']
        widgets={'comment': forms.Textarea(attrs={'cols': 30, 'rows': 2})}


class GeneralFeedbackForm(forms.Form):
    """Form for general feedback"""

    comment = forms.CharField(widget=forms.Textarea(attrs={'cols':'64'}), required=False)
#    video = VideoUploadToFLVField(required=False, widget=forms.FileInput(attrs={'size':'60'}))


class SignFeedbackForm(forms.ModelForm):
    """Form for input of sign feedback"""

    class Meta:
        model = SignFeedback
        exclude = ['name', 'kind', 'user', 'status']

class MissingSignFeedbackForm(forms.ModelForm):

    class Meta:
        model = MissingSignFeedback
        exclude = ['user', 'status']

class InterpreterFeedbackForm(forms.ModelForm):

    class Meta:
        model = InterpreterFeedback
        fields = ['comment']
        widgets={'comment': forms.Textarea(attrs={'cols': 30, 'rows': 2})}

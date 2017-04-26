from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.generic.edit import CreateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import GeneralFeedback, MissingSignFeedback, SignFeedback, InterpreterFeedback
from .forms import MissingSignFeedbackForm, SignFeedbackForm, InterpreterFeedbackForm


def index(request):
    return render(request, "feedback/index.html",
        {"language": settings.LANGUAGE_NAME,
        "country": settings.COUNTRY_NAME,})


class GeneralFeedbackCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''
    This class implements the general feedback form.
    '''
    model = GeneralFeedback
    fields = ["comment", "video"]
    success_url = reverse_lazy("feedback:generalfeedback")
    success_message = "Thanks for your comment. We value your contribution."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GeneralFeedbackCreate, self).form_valid(form)


@login_required
def missingsign(request):
    if request.method == "POST":
        form = MissingSignFeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            msfeedback = form.save(commit=False)
            msfeedback.user = request.user
            msfeedback.save()
            success_message = 'Thank you for your feedback. Note that addressing your feedback may take some time depending on the level of requests.'
            messages.success(request, success_message)
            return HttpResponseRedirect(reverse('feedback:missingsign'))
    # Any other kind of request goes here
    else:
        form = MissingSignFeedbackForm()
    return render(request, 'feedback/missingsign_form.html',
                               {
                                'language': settings.LANGUAGE_NAME,
                                'country': settings.COUNTRY_NAME,
                                'title':"Report a Missing Sign",
                                'form': form
                                })

@login_required
def wordfeedback(request, keyword, n):
    if request.method == "POST":
        form = SignFeedbackForm(request.POST)
        if form.is_valid():
            # This is the name of the sign.
            name = '%s-%s'%(keyword, n)
            save_signfeedback(request, form, name)
            messages.success(request, 'Thank you for your comment. We value your contribution')
            return HttpResponseRedirect(reverse('feedback:wordfeedback',
                kwargs={'keyword': keyword, 'n': n}))
   # Any other kind of request goes here
    else:
        form = SignFeedbackForm()
    return render(request, "feedback/signfeedback_form.html", {"form": form})

@login_required
def glossfeedback(request, n):
    if request.method == "POST":
        form = SignFeedbackForm(request.POST)
        if form.is_valid():
            # This is the name of the gloss.
            name = str(n)
            save_signfeedback(request, form, name)
            messages.success(request, 'Thank you for your comment. We value your contribution')
            return HttpResponseRedirect(reverse('feedback:glossfeedback', kwargs={'n': n}))
   # Any other kind of request goes here
    else:
        form = SignFeedbackForm()
    return render(request, "feedback/signfeedback_form.html", {"form": form})


def save_signfeedback(request, form, name):
    '''
    Do the work of saving feedback for a sign or gloss.
    '''
    form_to_save = form.save(commit=False)
    form_to_save.user= request.user
    form_to_save.name = name
    form_to_save.save()

@permission_required('feedback.delete_generalfeedback')
def showfeedback(request):
    '''
    View to list the feedback that's been left on the site.
    '''
    general = GeneralFeedback.objects.filter(status='unread')
    missing = MissingSignFeedback.objects.filter(status='unread')
    signfb = SignFeedback.objects.filter(status__in=('unread', 'read'))
    return render(request, "feedback/show.html",
        {'general': general,
         'missing': missing,
         'signfb': signfb
        }
    )



@permission_required('feedback.delete_generalfeedback')
def delete(request, kind, id):
    '''
    Mark a feedback item as deleted.
    kind can be either 'sign', 'general' or 'missingsign'.
    '''
    if kind == 'sign':
        kind = SignFeedback
    elif kind == 'general':
        kind = GeneralFeedback
    elif kind == 'missingsign':
        kind = MissingSignFeedback
    else:
        # Django treats this as a 500 error, and
        # tries to load 500.html stored in the root
        # template directory of the website.
        raise ValueError()
    feedback_to_delete = get_object_or_404(kind, pk=id)
    # mark as deleted
    feedback_to_delete.status = 'deleted'
    feedback_to_delete.save()
    # return to referer
    if 'HTTP_REFERER' in request.META:
        url = request.META['HTTP_REFERER']
    else:
        url = '/'
    return redirect(url)



@login_required
def interpreterfeedback(request, glossid=None):

    if request.method == "POST":

        if 'action' in request.POST and 'delete_all' in request.POST['action']:
            fbset = InterpreterFeedback.objects.filter(glossid=glossid)
            fbset.delete()
        elif 'action' in request.POST and 'delete' in request.POST['action']:
            fbid = request.POST['id']
            fb = get_object_or_404(InterpreterFeedback, pk=fbid)
            fb.delete()
        else:
            form = InterpreterFeedbackForm(request.POST, request.FILES)
            if form.is_valid():
                fb = form.save(commit=False)
                fb.user = request.user
                fb.glossid = glossid
                fb.save()

        # redirect to the gloss page
        return HttpResponseRedirect(reverse('dictionary:admin_gloss_view', kwargs={'pk': glossid}))
    else:

        # generate a page listing the feedback from interpreters

        notes = InterpreterFeedback.objects.all()

        general = GeneralFeedback.objects.filter(status='unread', user__groups__name='Interpreter')
        missing = MissingSignFeedback.objects.filter(status='unread', user__groups__name='Interpreter')
        signfb = SignFeedback.objects.filter(status='unread', user__groups__name='Interpreter')

        return render(request, 'feedback/interpreter.html',
                                   {'notes': notes,
                                    'general': general,
                                    'missing': missing,
                                    'signfb': signfb,
                                   }
                               )

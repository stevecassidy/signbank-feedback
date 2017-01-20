from django.conf.urls import url

from feedback import views

app_name = "feedback"
urlpatterns = [
    # ex: /
    url(r"^$", views.index, name="index"),
    # ex: generalfeedback/
    url(r"^generalfeedback/$", views.GeneralFeedbackCreate.as_view(),
        name="generalfeedback"),
    # ex: show/
    url(r'^show', views.showfeedback, name = 'showfeedback'),
    # ex: general/delete/1/
    url(r'^(?P<kind>general|sign|missingsign)/delete/(?P<id>\d+)/$',
    views.delete, name = 'delete'),
    # ex: missingsign/
    url(r'^missingsign/$', views.missingsign,
        name='missingsign'),
    # ex: sign/abscond-1/
    url(r'^word/(?P<keyword>.+)-(?P<n>\d+)/$', views.wordfeedback,
        name = 'wordfeedback'),
    # ex: gloss/1
    url(r'^gloss/(?P<n>\d+)/$', views.glossfeedback,
        name = 'glossfeedback'),

    url(r'^interpreter/(?P<glossid>\d+)', views.interpreterfeedback, name='intnote'),
    url(r'^interpreter.html', views.interpreterfeedback, name='intnotelist'),


]

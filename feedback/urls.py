from django.urls import path, re_path

from feedback import views

app_name = "feedback"
urlpatterns = [
    # ex: /
    path("", views.index, name="index"),
    # ex: generalfeedback/
    path("generalfeedback/", views.GeneralFeedbackCreate.as_view(), name="generalfeedback"),
    # ex: show/
    path('show/', views.showfeedback, name = 'showfeedback'),
    # ex: general/delete/1/
    re_path(r'^(?P<kind>general|sign|missingsign)/delete/(?P<id>\d+)/$',
    views.delete, name = 'delete'),
    # ex: missingsign/
    path('missingsign/', views.missingsign, name='missingsign'),
    # ex: sign/abscond-1/
    path('word/<keyword>-<int:n>/', views.wordfeedback, name = 'wordfeedback'),
    # ex: gloss/1
    path('gloss/<int:n>/', views.glossfeedback, name = 'glossfeedback'),

    path('interpreter/<int:glossid>', views.interpreterfeedback, name='intnote'),
    path('interpreter.html', views.interpreterfeedback, name='intnotelist'),


]

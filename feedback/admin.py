from django.contrib import admin

from feedback.models import GeneralFeedback, SignFeedback, MissingSignFeedback, InterpreterFeedback


class GeneralFeedbackAdmin(admin.ModelAdmin):
   list_display = ['user', 'date', 'comment']
   list_filter = ['user']
admin.site.register(GeneralFeedback, GeneralFeedbackAdmin)


class SignFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'name']
    list_filter = ['user']
admin.site.register(SignFeedback, SignFeedbackAdmin)


class MissingSignFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']
    list_filter = ['user']
admin.site.register(MissingSignFeedback, MissingSignFeedbackAdmin)


class InterpreterFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']
    list_filter = ['user']
admin.site.register(InterpreterFeedback, MissingSignFeedbackAdmin)

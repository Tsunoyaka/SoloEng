from django.contrib import admin

from .models import Exams, Questions, AnswerOptions, UserAnswer



admin.site.register(Exams)
admin.site.register(Questions)
admin.site.register(AnswerOptions)
admin.site.register(UserAnswer)
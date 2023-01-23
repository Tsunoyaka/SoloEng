from django.contrib import admin

from .models import (
    CoursLevels, 
    Courses, 
    RatingCours, 
    Modules, 
    Lessons,
    CoursProgres, 
    JoinCours
    )

admin.site.register(CoursLevels)
admin.site.register(Courses)
admin.site.register(RatingCours)
admin.site.register(Modules)
admin.site.register(Lessons)
admin.site.register(CoursProgres)
admin.site.register(JoinCours)
from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import (
   CoursLevelViewSet,
   CoursesViewSet,
   ModulesViewset,
   LessonsViewSet,
   CoursProgresAPIView,
   JoinCoursViewSet
   )


router = DefaultRouter()
router.register('courslevel', CoursLevelViewSet)
router.register('crud-cours', CoursesViewSet)
router.register('cours-module', ModulesViewset)
router.register('cours-lessons', LessonsViewSet)
router.register('join-cours', JoinCoursViewSet)

urlpatterns = [
    path('cours-progres/', CoursProgresAPIView.as_view())
]

urlpatterns += router.urls


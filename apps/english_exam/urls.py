from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import (
   ExamsViewSet, 
   QuestionsViewSet, 
   AnswerOptionsViewSet, 
   UserAnswerAPIView,
   UserScoreAPIView
   )


router = DefaultRouter()
router.register('exams', ExamsViewSet, 'exams-url')
router.register('questions', QuestionsViewSet, 'questions-url')
router.register('answer-options', AnswerOptionsViewSet, 'options-url')


urlpatterns = [
   path('answer/<str:slug>/', UserAnswerAPIView.as_view()),
   path('user-score/', UserScoreAPIView.as_view()),
]

urlpatterns += router.urls


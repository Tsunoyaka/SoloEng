from django.db import models
from slugify import slugify
from .utils import get_time
from django.contrib.auth import get_user_model
from apps.english_cours.models import Courses


User = get_user_model()


class Exams(models.Model):
    con_cours = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='rel_exam')


    def __str__(self) -> str:
        return f'Тест для курса: {self.con_cours.title}'


class Questions(models.Model):
    con_exam = models.ForeignKey(to=Exams, on_delete=models.CASCADE, related_name='rel_questions')
    question = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500, primary_key=True, blank=True)


    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question + get_time())
        super().save(*args, **kwargs)

    
    def __str__(self) -> str:
        return self.question


class AnswerOptions(models.Model):
    con_question = models.ForeignKey(to=Questions, on_delete=models.CASCADE, related_name='rel_options')
    options = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    slug = models.SlugField(max_length=500, primary_key=True, blank=True)


    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.options + get_time())
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.options


class UserAnswer(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='rel_answer'
    )
    con_courses = models.ForeignKey(
        to=Courses,
        on_delete=models.CASCADE,
        related_name='rel_answer'
    )
    score = models.SmallIntegerField()


    def __str__(self) -> str:
        return f'Пользователь {self.user} получил {self.score} очков за тест в курсе {self.con_courses} '
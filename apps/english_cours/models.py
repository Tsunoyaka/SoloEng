from django.db import models
from .utils import get_time
from slugify import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class CoursLevels(models.Model):
    title = models.CharField(max_length=10, primary_key=True)


    def __str__(self) -> str:
        return self.title


class Courses(models.Model):
    cours_lev = models.ForeignKey(to=CoursLevels, on_delete=models.CASCADE, related_name='cours_level')
    price = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='cours_img')
    slug = models.SlugField(max_length=500, primary_key=True, blank=True)


    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.title



class RatingCours(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='rating_cours')
    con_cours = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='rating_cours')
    rating = models.SmallIntegerField()


    def __str__(self) -> str:
        return f'Рейтинг курса {self.con_cours.title} составляет {self.rating}'


class Modules(models.Model):
    con_cours = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='modul_cours')
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Lessons(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='lessons_img')
    link = models.CharField(max_length=500)
    desc = models.TextField()
    con_module = models.ForeignKey(to=Modules, on_delete=models.CASCADE, related_name='lessons_cours')
    con_cours = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='lessons_cours')
    slug = models.SlugField(max_length=500, primary_key=True, blank=True)


    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.title


class CoursProgres(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='progres')
    con_cours = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='progres')
    con_lessons = models.ForeignKey(to=Lessons, on_delete=models.CASCADE, related_name='progres')


    def __str__(self) -> str:
        return f'Пользователь {self.user.username} просмотрел видеоурок {self.con_lessons.title} из курса {self.con_cours.title} '


class JoinCours(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_join')
    cours = models.ForeignKey(to=Courses, on_delete=models.CASCADE, related_name='user_join')
    process = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)


    def save(self,*args, **kwargs):
        if self.complete is False:
            self.process = True
        else:
            self.process = False
            self.complete = True
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Пользователь {self.user.username} записан на курс {self.cours.title}'
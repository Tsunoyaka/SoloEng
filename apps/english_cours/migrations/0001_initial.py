# Generated by Django 4.1.5 on 2023-01-23 12:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('price', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to='cours_img')),
                ('slug', models.SlugField(blank=True, max_length=500, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='CoursLevels',
            fields=[
                ('title', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='RatingCours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField()),
                ('con_cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_cours', to='english_cours.courses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating_cours', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('con_cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modul_cours', to='english_cours.courses')),
            ],
        ),
        migrations.CreateModel(
            name='Lessons',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='lessons_img')),
                ('link', models.CharField(max_length=500)),
                ('desc', models.TextField()),
                ('slug', models.SlugField(blank=True, max_length=500, primary_key=True, serialize=False)),
                ('con_cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons_cours', to='english_cours.courses')),
                ('con_module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons_cours', to='english_cours.modules')),
            ],
        ),
        migrations.CreateModel(
            name='JoinCours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process', models.BooleanField(default=False)),
                ('complete', models.BooleanField(default=False)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_join', to='english_cours.courses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_join', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoursProgres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('con_cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progres', to='english_cours.courses')),
                ('con_lessons', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progres', to='english_cours.lessons')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progres', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='courses',
            name='cours_lev',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cours_level', to='english_cours.courslevels'),
        ),
    ]

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Avg

from .models import (
    CoursLevels, 
    Courses, 
    RatingCours, 
    Modules, 
    Lessons,
    CoursProgres, 
    JoinCours
    )
from apps.english_exam.models import UserAnswer, Exams
from apps.english_exam.serializers import ExamsSerializer

User = get_user_model()


class CoursLevelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursLevels
        fields = '__all__'  


class CoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = '__all__'  


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating = instance.rating_cours.aggregate(Avg('rating'))['rating__avg']
        if rating:
            representation['rating'] = round(rating, 1)
        else:
            representation['rating'] = 0.0
        try:
            user = self.context['request'].user
            progres = instance.progres.filter(user=user).count()
            all_ = instance.lessons_cours.all().count()
            if progres != 0:
                representation['progres'] = round(progres / all_ * 100, 1)
        except:
            None
        return representation


class CoursesRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courses
        fields = '__all__'  


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating = instance.rating_cours.aggregate(Avg('rating'))['rating__avg']
        if rating:
            representation['rating'] = round(rating, 1)
        else:
            representation['rating'] = 0.0
        try:
            user = self.context['request'].user
            progres = instance.progres.filter(user=user).count()
            all_ = instance.lessons_cours.all().count()
            if progres != 0:
                representation['progres'] = round(progres / all_ * 100, 1)
        except:
            None
        representation['moduls'] = ModulesSerializer(instance.modul_cours.all(), many=True).data
        representation['final_test'] = ExamsSerializer(instance.rel_exam.all(), many=True).data 
        return representation

class RatingCoursSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        source='user.username'
    )


    class Meta:
        model = RatingCours
        fields = '__all__'  


    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating')
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError(
                'Wrong value! Rating must be between 1 and 5'
                )
        return attrs


    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class ModulesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Modules
        fields = '__all__'


    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        representation['lessons_is_module'] = LessonsSerializer(instance.lessons_cours.all(), many=True).data
        return representation

class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lessons
        fields = '__all__'


class CoursProgresSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


    class Meta:
        model = CoursProgres
        fields = '__all__'

    def create_(self, validate_data):
        user = self.validated_data['user']
        con_cours = self.validated_data['con_cours']
        con_lessons = self.validated_data['con_lessons']
        cours_prog = CoursProgres.objects.filter(con_cours=con_cours, con_lessons=con_lessons).exists()
        cours_all = CoursProgres.objects.filter(user=user).count()
        table_score = UserAnswer.objects.filter(user=user)
        user_score = User.objects.get(email=user.email)
        score_ = []
        if table_score:
            for i in table_score:
                score_.append(i.score)
            user_score.score = sum(score_) * 20 + cours_all * 10
            user_score.save()
        if cours_prog is False:
            CoursProgres.objects.create(**self.validated_data)
        
        # return None


class JoinCoursSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.email'
    )

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


    class Meta:
        model = JoinCours
        fields = '__all__'
 



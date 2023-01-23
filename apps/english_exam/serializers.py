from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Exams, Questions, AnswerOptions, UserAnswer

from apps.english_cours.models import JoinCours, CoursProgres


User = get_user_model()


class ExamsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exams
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['questions'] = QuestionsSerializer(
            instance.rel_questions.all(), many=True).data
        return representation


class QuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['answer_options'] = AnswerSerializer(
            instance.rel_options.all(), many=True).data
        return representation


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerOptions
        fields = '__all__'

 
class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = '__all__'


    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )


    def validate(self, attrs):
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


    def score(self):
        score = self.validated_data['score']
        courses = self.validated_data['con_courses']
        user = self.validated_data['user']
        table = UserAnswer.objects.filter(user=user, con_courses=courses)
        table_score = UserAnswer.objects.filter(user=user)
        user_score = User.objects.get(email=user.email)
        cours_all = CoursProgres.objects.filter(user=user).count()
        score_ = []
        if score >= 6:
            complete = JoinCours.objects.get(user=user, cours=courses)
            complete.complete = True
            complete.save()
        if table:
            table[0].score = score if score > table[0].score else table[0].score
            table[0].save()
        if table_score:
            for i in table_score:
                score_.append(i.score)
            user_score.score = sum(score_) * 20 + cours_all * 10
            user_score.save()
        else:
            usr = UserAnswer.objects.create(**self.validated_data)
    

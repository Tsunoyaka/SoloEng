from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Courses,
    Exams,
    Questions,
    AnswerOptions,
    UserAnswer
)
from .serializers import (
    ExamsSerializer, 
    QuestionsSerializer, 
    AnswerSerializer, 
    UserAnswerSerializer
    )


class ExamsViewSet(ModelViewSet):
    queryset = Exams.objects.all()
    serializer_class = ExamsSerializer


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class QuestionsViewSet(ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()



class AnswerOptionsViewSet(ModelViewSet):
    queryset = AnswerOptions.objects.all()
    serializer_class = AnswerSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class UserAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        answer = AnswerOptions.objects.get(slug=slug)
        return Response(answer.correct, status=status.HTTP_200_OK)


class UserScoreAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserAnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.score()
            return Response(
                'Ответ был записан в таблицу',
                status=status.HTTP_200_OK
            )


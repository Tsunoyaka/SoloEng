from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema


from .models import (
    CoursLevels, 
    Courses, 
    RatingCours, 
    Modules, 
    Lessons,
    CoursProgres, 
    JoinCours
    )

from .serializers import (
    CoursLevelsSerializer,
    CoursesSerializer,
    RatingCoursSerializer,
    ModulesSerializer,
    LessonsSerializer,
    CoursProgresSerializer,
    JoinCoursSerializer,
    CoursesRetrieveSerializer
    )


class CoursLevelViewSet(ModelViewSet):
    queryset = CoursLevels.objects.all()
    serializer_class = CoursLevelsSerializer
    permission_classes = [AllowAny]


class CoursesViewSet(ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer


    def get_serializer_class(self):
        if self.action == 'list':
            return CoursesSerializer
        elif self.action == 'create':
            return CoursesSerializer
        elif self.action == 'retrieve':
            return CoursesRetrieveSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


    @action(methods=['POST', 'PATCH'], detail=True, url_path='set-rating')
    def set_rating(self, request, pk=None):
        data = request.data.copy()
        data['con_cours'] = pk # TODO
        serializer = RatingCoursSerializer(data=data, context={'request': request})
        rate = RatingCours.objects.filter(
            user=request.user,
            con_cours=pk
        ).first()
        if serializer.is_valid(raise_exception=True):
            if rate and request.method == 'POST':
                return Response(
                    {'detail': 'Rating object exists. Use PATCH method'}
                )
            elif rate and request.method == 'PATCH':
                serializer.update(rate, serializer.validated_data)
                return Response('Updated')
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Rating object does not exist. Use POST method.'})





class ModulesViewset(ModelViewSet):
    queryset = Modules.objects.all()
    serializer_class = ModulesSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class LessonsViewSet(ModelViewSet):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticated]
        if self.action in ['create']:
            self.permission_classes = [IsAdminUser]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


@swagger_auto_schema(CoursProgresSerializer)
class CoursProgresAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CoursProgresSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.create_(serializer.data)
        return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )   


class JoinCoursViewSet(ModelViewSet):
    queryset = JoinCours.objects.all()
    serializer_class = JoinCoursSerializer
    permission_classes = [IsAuthenticated]


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context






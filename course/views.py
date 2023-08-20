# from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from course.models import Course, Lesson
from course.pagination import MyPagination
from course.permissions import CanCreate, IsModerator, IsOwner
from course.serializers import CourseSerializer, LessonSerializer
from course.services import get_users_emails_from_subs
from course.tasks import send_course_update_email
from users.models import Subscription


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = MyPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def update(self, request, *args, **kwargs):
        
        subs = Subscription.objects.filter(user=request.user)
        emails = get_users_emails_from_subs(subs)
        send_course_update_email.delay(emails)
        
        return super().update(request, *args, **kwargs)

    def get_queryset(self):

        if self.request.user.groups.filter(name='moderator').exists():
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):

        permission_classes = (IsAuthenticated, )

        if self.action == 'create':
            permission_classes = (CanCreate, )

        elif self.action == 'destroy':
            permission_classes = (CanCreate, IsOwner)

        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = (IsModerator | IsOwner, )

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer

    permission_classes = (CanCreate, AllowAny)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = MyPagination

    def get_queryset(self):

        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer

    permission_classes = (IsOwner | IsModerator, )

    def get_queryset(self):

        if self.request.user.groups.filter(name='moderator').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = (IsOwner | IsModerator, )


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()

    permission_classes = (IsOwner, )

# from django.shortcuts import render
from course.models import Course
from course.serializers import CourseSerializer

from rest_framework import viewsets


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

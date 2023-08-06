from course.models import Course

from lesson.serializers import LessonSerializer

from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'name', 'description', 'image', 'amount_of_lessons', 'lessons',
        )

    lessons = LessonSerializer(many=True)
    amount_of_lessons = serializers.SerializerMethodField()

    def get_amount_of_lessons(self, obj):
        return obj.lessons.count()

from course.models import Course, Lesson

from rest_framework import serializers


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'name', 'description', 'image', 'amount_of_lessons', 'lessons',
        )

    lessons = LessonSerializer(many=True, required=False)
    amount_of_lessons = serializers.SerializerMethodField()

    def get_amount_of_lessons(self, obj):
        return obj.lessons.count()

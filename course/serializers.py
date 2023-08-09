from rest_framework import serializers

from course.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'id', 'name', 'description', 'image', 'amount_of_lessons', 'lessons', 'owner',
        )

    lessons = LessonSerializer(many=True, required=False)
    amount_of_lessons = serializers.SerializerMethodField()

    def get_amount_of_lessons(self, obj):
        return obj.lessons.count()

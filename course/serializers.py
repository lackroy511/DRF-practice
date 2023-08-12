from rest_framework import serializers

from course.models import Course, Lesson
from course.validators import IsURLValidator, VideoURLValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

        validators = [
            VideoURLValidator(field_name='video_url'),
            IsURLValidator(),
        ]


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'id', 'name', 'description', 'image', 'video_url', 'amount_of_lessons', 'lessons', 'owner', 'is_subscribed',
        )

        validators = [
            VideoURLValidator(field_name='video_url'),
            IsURLValidator(),
        ]

    lessons = LessonSerializer(many=True, required=False)
    amount_of_lessons = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_amount_of_lessons(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        # Если у текущего курса есть подписка с текущем пользователем:
        if obj.subscriptions.filter(user=self.context['request'].user).exists():
            return True

        return False

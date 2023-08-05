from rest_framework import serializers

from course.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('name', 'description', 'image', 'amount_of_lessons')

    amount_of_lessons = serializers.SerializerMethodField()

    def get_amount_of_lessons(self, obj):
        return obj.course.count()

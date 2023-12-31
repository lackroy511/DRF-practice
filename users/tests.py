from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course, Lesson
from users.models import Subscription, User


class SubscriptionPositiveTestCase(APITestCase):
    
    def setUp(self) -> None:
        
        self.user = User.objects.create(
            email='test@test.com',
        )
        self.user.set_password('test')
        self.user.save()
        
        self.course = Course.objects.create(
            name='test course',
            description='test course description',
        )

        self.lesson = Lesson.objects.create(
            name='test',
            description='test description',
            video_url='https://www.youtube.com',
            owner=self.user,
            course=self.course,
        )
        
    def test_subscription_create(self):
        
        self.client.force_authenticate(user=self.user)
        
        data = {
            'course': self.course.pk,
            'user': self.user.pk,
        }
        
        response = self.client.post(
            path='/user/sub/create/', data=data,
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('course'), self.course.pk)
        self.assertEqual(response.json().get('user'), self.user.pk)
        self.assertEqual(response.json().get('course_name'), self.course.name)

    def test_subscription_delete(self):
        
        subscription = Subscription.objects.create(
            course=self.course,
            user=self.user,
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(
            f'/user/sub/delete/{subscription.pk}/',
        )
        
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Subscription.objects.all().exists(),
        )


class SubscriptionNegativeTestCase(APITestCase):
    
    def setUp(self) -> None:
        
        self.user = User.objects.create(
            email='test@test.com',
        )
        self.user.set_password('test')
        self.user.save()
        
        self.course = Course.objects.create(
            name='test course',
            description='test course description',
        )

        self.lesson = Lesson.objects.create(
            name='test',
            description='test description',
            video_url='https://www.youtube.com',
            owner=self.user,
            course=self.course,
        )
    
    def test_subscription_create(self):
    
        self.client.force_authenticate(user=self.user)
        
        data = {
            'course': self.course.pk,
            'user': self.user.pk,
        }
        
        response = self.client.post(
            path='/user/sub/create/', data=data,
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post(
            path='/user/sub/create/', data=data,
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

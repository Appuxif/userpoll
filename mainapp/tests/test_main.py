from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class TestUserTokenAuth(APITestCase):
    """Тест получения токена через API"""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            'testuser',
            'testuser@example.com',
            'testuserpwd',
        )

    def test_token_auth(self):
        """Тест получения токена через API"""
        response = self.client.post(
            '/api/token/auth/',
            {
                'username': 'testuser',
                'password': 'testuserpwd',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = Token.objects.get(user__username='testuser')
        self.assertEqual(response.data['token'], token.key)

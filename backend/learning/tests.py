from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
# Create your tests here.

class AuthenticationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email = "test@example.com",
            password= "TestPassword123!"
        )

    def test_register_user(self):
        response = self.client.post(
            "/api/v1/auth/register/",
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "NewPassword123!"
            },
            format = "json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_duplicate_email_rejected(self):
        response = self.client.post(
            "/api/v1/auth/register/",
            {
                "username": "anotheruser",
                "email": "test@example.com",
                "password": "AnotherPassword123!"
            },
            format = "json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_correct_password(self):
        response = self.client.post(
            "/api/v1/auth/login/",
            {
                "username": "testuser",
                "password": "TestPassword123!"
            },
            format = "json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_incorrect_password(self):
        response = self.client.post(
            "/api/v1/auth/login/",
            {
                "username": "testuser",
                "password": "WrongPassword123!"
            },
            format = "json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_current_user_requires_authentication(self):
        response = self.client.get("/api/v1/auth/me/")
        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ]
        )

    def test_current_user_returns_logged_in_user(self):
        self.client.login(
            username = "testuser",
            password = "TestPassword123!"
        )
        response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["username"],
            "testuser"
        )
        self.assertEqual(
            response.data["email"],
            "test@example.com"
        )

    def test_logout_invalidates_session(self):
        self.client.login(
            username = "testuser",
            password = "TestPassword123!"
        )

        response = self.client.post("/api/v1/auth/logout/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        response = self.client.get("/api/v1/auth/me/")
        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ]
        )
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Letter, Lesson, QuizAttempt, LessonLetter
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

class QuizSecurityTests(APITestCase):

    def setUp(self):
        self.user_a = User.objects.create_user(
            username = "usera",
            email = "usera@example.com",
            password = "Password123!"
        )
        self.user_b = User.objects.create_user(
            username = "userb",
            email = "userb@example.com",
            password = "Password123!"
        )
        self.lesson = Lesson.objects.create(
            title = "Test Lesson",
            description = "Test lesson",
            display_order = 1,
            status = Lesson.PUBLISHED
        )
        self.letter = Letter.objects.create(
            character = "அ",
            spoken_name = "ahna",
            romanization = "a",
            category = Letter.UYIR,
            display_order = 1
        )
        self.quiz_attempt = QuizAttempt.objects.create(
            user = self.user_a,
            lesson = self.lesson,
            score = 1,
            total_questions = 1,
            completed_at = timezone.now()
        )
        self.letter_b = Letter.objects.create(
            character = "ஆ",
            spoken_name = "ahvana",
            romanization = "aa",
            category = Letter.UYIR,
            display_order = 2
        )
        LessonLetter.objects.create(
            lesson = self.lesson,
            letter = self.letter,
            display_order = 1
        )
        LessonLetter.objects.create(
            lesson = self.lesson,
            letter = self.letter_b,
            display_order = 2
        )

    def test_quiz_history_requires_auth(self):
        response = self.client.get("/api/v1/quiz-attempts/")

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN
            ]
        )

    def test_user_cannot_access_another_users_quiz_result(self):
        self.client.login(
            username = "userb",
            password = "Password123!"
        )
        response = self.client.get(
            f"/api/v1/quiz-attempts/{self.quiz_attempt.id}/"
        )
        self.assertEqual (
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_quiz_creation_does_not_expose_correct_ans(self):
        self.client.login(
            username = "usera",
            password = "Password123!"
        )

        response = self.client.post(
            f"/api/v1/lessons/{self.lesson.id}/quiz-attempts/",
            {},
            format = "json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        for question in response.data["question_attempts"]:
            self.assertNotIn("correct_answer", question)
            self.assertNotIn("is_correct", question)

    def test_completed_quiz_returns_result_fields(self):
        self.client.login(
            username = "usera",
            password = "Password123!"
        )
        create_response = self.client.post (
            f"/api/v1/lessons/{self.lesson.id}/quiz-attempts/",
            {},
            format = "json"
        )
        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED
        )
        quiz_id = create_response.data["id"]
        questions = create_response.data["question_attempts"]

        answers = [
            {
                "question_id": question["id"],
                "selected_answer": question["options"][0]
            }
            for question in questions 
        ]

        submit_response = self.client.post(
            f"/api/v1/quiz-attempts/{quiz_id}/submit/",
            {
                "answers": answers,
            },
            format = "json"
        )

        self.assertEqual(
            submit_response.status_code,
            status.HTTP_200_OK
        )
        for question in submit_response.data["question_attempts"]:
            self.assertIn("selected_answer", question)
            self.assertIn("correct_answer", question)
            self.assertIn("is_correct", question)

    def test_duplicate_question_ids_are_rejected(self):
        self.client.login(
            username = "usera",
            password = "Password123!"
        )
        create_response = self.client.post(
            f"/api/v1/lessons/{self.lesson.id}/quiz-attempts/",
            {},
            format = "json"
        )
        quiz_id = create_response.data["id"]
        questions = create_response.data["question_attempts"]
        duplicate_question_id = questions[0]["id"]
        response = self.client.post(
            f"/api/v1/quiz-attempts/{quiz_id}/submit/",
            {
                "answers": [
                    {
                        "question_id": duplicate_question_id,
                        "selected_answer": questions[0]["options"][0]
                    },
                    {
                        "question_id": duplicate_question_id,
                        "selected_answer": questions[0]["options"][0]
                    }
                ]
            },
            format = "json"
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_invalid_answer_is_rejected(self):
        self.client.login(
            username = "usera",
            password = "Password123!"
        )
        create_response = self.client.post(
            f"/api/v1/lessons/{self.lesson.id}/quiz-attempts/",
            {},
            format = "json"
        )
        quiz_id = create_response.data["id"]
        questions = create_response.data["question_attempts"]

        answers = []

        for question in questions:
            answers.append(
                {
                    "question_id": question["id"],
                    "selected_answer": question["options"][0]
                }
            )

        answers[0]["selected_answer"] = "not-valid-option"

        response = self.client.post(
            f"/api/v1/quiz-attempts/{quiz_id}/submit/",
            {
                "answers": answers
            },
            format = "json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
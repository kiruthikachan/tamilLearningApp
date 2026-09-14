from django.urls import path
from .views import letter_list, lesson_list, lesson_detail, create_quiz_attempt, submit_quiz_attempt, quiz_attempt_list, quiz_attempt_detail

urlpatterns = [
    path("letters/", letter_list, name="letter-list"),
    path("lessons/", lesson_list, name="lesson-list"),
    path("lessons/<int:lesson_id>/", lesson_detail, name = "lesson-detail"),
    path("lessons/<int:lesson_id>/quiz-attempts/", create_quiz_attempt, name="create-quiz-attempt"),
    path("quiz-attempts/<int:attempt_id>/submit/", submit_quiz_attempt, name="submit-quiz-attempt"),
    path("quiz-attempts/", quiz_attempt_list, name="quiz-attempt-list"),
    path("quiz-attempts/<int:attempt_id>/", quiz_attempt_detail, name = "quiz-attempt-detail")
]
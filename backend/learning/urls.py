from django.urls import path
from .views import letter_list, lesson_list, lesson_detail, create_quiz_attempt, submit_quiz_attempt

urlpatterns = [
    path("letters/", letter_list, name="letter-list"),
    path("lessons/", lesson_list, name="lesson-list"),
    path("lessons/<int:lesson_id>/", lesson_detail, name = "lesson-detail"),
    path("lessons/<int:lesson_id>/quiz-attempts/", create_quiz_attempt, name="create-quiz-attempt"),
    path("quiz-attempts/<int:attempt_id>/submit/", submit_quiz_attempt, name="submit-quiz-attempt"),
]
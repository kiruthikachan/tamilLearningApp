from django.urls import path
from .views import letter_list, lesson_list, lesson_detail

urlpatterns = [
    path("letters/", letter_list, name="letter-list"),
    path("lessons/", lesson_list, name="lesson-list"),
    path("lessons/<int:lesson_id>/", lesson_detail, name = "lesson-detail"),
]
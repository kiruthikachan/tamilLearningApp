from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Letter, ExampleWord, Lesson, LessonLetter
from .serializers import LetterSerializer, LessonListSerializer, LessonSerializer

# Create your views here.

@api_view(["GET"])
def letter_list(request):
    letters = (
            Letter.objects
            .filter(is_active = True)
            .prefetch_related(
                Prefetch(
                    "example_words", 
                    queryset=ExampleWord.objects
                    .filter(is_active=True)
                    .order_by("display_order")
                )
            )
            .order_by("display_order")
    )

    serializer = LetterSerializer(letters,many=True)

    return Response(serializer.data)

@api_view(["GET"])
def lesson_list(request):
    lessons = (
        Lesson.objects
        .filter(status=Lesson.PUBLISHED)
        .order_by("display_order")
    )
    serializer = LessonListSerializer(lessons,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def lesson_detail(request, lesson_id):

    lesson_letters = (
        LessonLetter.objects
        .select_related("letter")
        .prefetch_related(
            Prefetch(
                "letter__example_words",
                queryset=ExampleWord.objects
                .filter(is_active=True)
                .order_by("display_order")
            )
        )
        .order_by("display_order")
    )

    try:
        lesson = (
            Lesson.objects
            .prefetch_related(
                Prefetch(
                    "lesson_letters",
                    queryset=lesson_letters
                )
            )
            .get(
                id=lesson_id,
                status=Lesson.PUBLISHED
            )
        )

    except Lesson.DoesNotExist:
        return Response(
            {"detail": "Lesson not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = LessonSerializer(lesson)
    return Response(serializer.data)
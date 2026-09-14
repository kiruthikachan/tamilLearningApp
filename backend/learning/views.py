import random
from django.db import transaction
from django.db.models import Prefetch
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Letter, ExampleWord, Lesson, LessonLetter, QuizAttempt, QuestionAttempt
from .serializers import LetterSerializer, LessonListSerializer, LessonSerializer, QuizAttemptSerializer, QuizResultSerializer, QuizHistorySerializer

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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_quiz_attempt(request,lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id, status= Lesson.PUBLISHED)
    except Lesson.DoesNotExist:
        return Response({"detail": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)
    lesson_letters = list(
        Letter.objects.filter(
            lesson_letters__lesson = lesson,
            is_active = True)
            .order_by("lesson_letters__display_order")
        )
    if len(lesson_letters) < 2:
        return Response({"detail": "This lesson does not have enough letters for a quiz."}, status=status.HTTP_400_BAD_REQUEST)
    with transaction.atomic():
        quiz_attempt = QuizAttempt.objects.create(user = request.user, lesson=lesson, total_questions = len(lesson_letters))
        for letter in lesson_letters:
            correct_answer = letter.romanization
            wrong_answers = [
                other_letter.romanization
                for other_letter in lesson_letters
                if other_letter.id != letter.id
            ]
            random.shuffle(wrong_answers)
            wrong_answers = wrong_answers[:3]
            options = wrong_answers + [correct_answer]
            random.shuffle(options)
            QuestionAttempt.objects.create(
                quiz_attempt = quiz_attempt,
                letter=letter,
                question_type = QuestionAttempt.SOUND,
                prompt = f"What does {letter.character} represent?",
                options = options,
                correct_answer = correct_answer
            )
    serializer = QuizAttemptSerializer(quiz_attempt)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_quiz_attempt(request, attempt_id):
    try:
        quiz_attempt = QuizAttempt.objects.get(
            id=attempt_id,
            user=request.user
        )
    except QuizAttempt.DoesNotExist:
        return Response({"detail": "Quiz attempt not found."}, status=status.HTTP_404_NOT_FOUND)
    if quiz_attempt.completed_at is not None:
        return Response({"detail": "This quiz has already been submitted."}, status=status.HTTP_400_BAD_REQUEST)
    answers = request.data.get("answers")
    if not isinstance(answers, list):
        return Response({"detail": "Answers must be provided as a list."}, status=status.HTTP_400_BAD_REQUEST)
    questions = {
        question.id: question
        for question in quiz_attempt.question_attempts.all()
    }
    if len(answers) != len(questions):
        return Response({"detail": "Every question must be answered."}, status=status.HTTP_400_BAD_REQUEST)
    submitted_question_ids = set()
    submitted_questions = []
    for answer in answers:
        question_id = answer.get("question_id")
        selected_answer = answer.get("selected_answer")
        if question_id in submitted_question_ids:
            return Response({"detail": f"Question {question_id} was submitted more than once."}, status=status.HTTP_400_BAD_REQUEST)
        question = questions.get(question_id)
        if question is None:
            return Response({"detail": f"Question {question_id} is not part of this quiz."}, status = status.HTTP_400_BAD_REQUEST)
        if selected_answer not in question.options:
            return Response({"detail": f"Invalid answer for question {question_id}."}, status=status.HTTP_400_BAD_REQUEST)
        submitted_question_ids.add(question_id)
        submitted_questions.append((question,selected_answer))
    score = 0
    with transaction.atomic():
        for question, selected_answer in submitted_questions:
            question.selected_answer = selected_answer
            question.is_correct = (
                selected_answer == question.correct_answer
            )
            question.answered_at = timezone.now()
            question.save()
            if question.is_correct:
                score += 1
        quiz_attempt.score = score
        quiz_attempt.completed_at = timezone.now()
        quiz_attempt.save()
    serializer = QuizResultSerializer(quiz_attempt)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def quiz_attempt_list(request):
    attempts = (
        QuizAttempt.objects
        .filter(user=request.user, completed_at__isnull = False)
        .select_related("lesson")
        .order_by("-started_at")
    )
    serializer = QuizHistorySerializer(attempts, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def quiz_attempt_detail(request, attempt_id):
    try:
        attempt = (
        QuizAttempt.objects
        .prefetch_related("question_attempts")
        .get(
            id = attempt_id,
            user = request.user,
            completed_at__isnull = False,
        )
    )
    except QuizAttempt.DoesNotExist:
        return Response(
            {"detail": "Quiz attempt not found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = QuizResultSerializer(attempt)
    return Response(serializer.data)

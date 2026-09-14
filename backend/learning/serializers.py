from rest_framework import serializers
from .models import Letter, ExampleWord, Lesson, LessonLetter, QuestionAttempt, QuizAttempt

class ExampleWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleWord
        fields = [
            "id",
            "word",
            "meaning",
            "romanization",
            "display_order",
        ]
class LetterSerializer(serializers.ModelSerializer):
    example_words = ExampleWordSerializer(many = True, read_only = True)
    class Meta:
        model = Letter
        fields = [
            "id",
            "character",
            "spoken_name",
            "romanization",
            "category",
            "display_order",
            "pronunciation_description",
            "is_active",
            "example_words"
        ]

class LessonLetterSerializer(serializers.ModelSerializer):
    letter = LetterSerializer(read_only=True)
    class Meta:
        model = LessonLetter
        fields = ["letter", "display_order",]

class LessonSerializer(serializers.ModelSerializer):
    lesson_letters = LessonLetterSerializer(many=True, read_only=True)
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "content",
            "display_order",
            "status",
            "lesson_letters",
        ]

class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "display_order",
        ]

class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAttempt
        fields = [
            "id",
            "letter",
            "question_type",
            "prompt",
            "options",
        ]

class QuestionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAttempt
        fields = [
            "id",
            "letter",
            "question_type",
            "prompt",
            "options",
            "selected_answer",
            "correct_answer",
            "is_correct",
        ]

class QuizAttemptSerializer(serializers.ModelSerializer):
    question_attempts = QuizQuestionSerializer(many=True, read_only = True)
    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "lesson",
            "started_at",
            "question_attempts",
        ]

class QuizResultSerializer(serializers.ModelSerializer):
    question_attempts = QuestionResultSerializer(many = True, read_only = True)
    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "lesson",
            "score",
            "total_questions",
            "started_at",
            "completed_at",
            "question_attempts",
        ]

class QuizHistorySerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source = "lesson.title", read_only = True)
    class Meta:
        model = QuizAttempt
        fields = [
            "id",
            "lesson",
            "lesson_title",
            "score",
            "total_questions",
            "started_at",
            "completed_at",
        ]
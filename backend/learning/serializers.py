from rest_framework import serializers
from .models import Letter, ExampleWord, Lesson, LessonLetter

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
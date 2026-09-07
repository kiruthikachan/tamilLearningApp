from rest_framework import serializers
from .models import Letter, ExampleWord

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
class letterSerializer(serializers.ModelSerializer):
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

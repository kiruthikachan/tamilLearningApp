from rest_framework import serializers
from .models import Letter

class letterSerializer(serializers.ModelSerializer):
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
        ]

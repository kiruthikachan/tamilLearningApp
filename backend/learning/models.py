from django.db import models

class Letter(models.Model):
    UYIR = "uyir"
    MEY = "mey"
    UYIR_MEY = "uyir_mey"
    AYTHAM = "aytham"
    CATEGORY_CHOICES = [
        (UYIR, "Uyir"),
        (MEY, "Mey"),
        (UYIR_MEY, "Uyir-Mey"),
        (AYTHAM, "Aytham"),
    ]
    character = models.CharField(max_length=10, unique=True)
    spoken_name = models.CharField(max_length=50)
    romanization = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    display_order = models.PositiveIntegerField()
    pronunciation_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.character} - {self.spoken_name}"

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

class ExampleWord(models.Model):
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name="example_words")
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100)
    romanization = models.CharField(max_length=100, blank=True)
    display_order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.word

class Lesson(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = [(DRAFT, "Draft"), (PUBLISHED, "Published"),]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class LessonLetter (models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_letters")
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE,related_name="lesson_letters")
    display_order = models.PositiveIntegerField(default = 1)
    class Meta:
        constraints = [models.UniqueConstraint(fields= ["lesson", "letter"], name = "unique_lesson_letter")]
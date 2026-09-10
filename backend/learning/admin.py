from django.contrib import admin
from .models import Letter, ExampleWord, Lesson, LessonLetter, QuizAttempt, QuestionAttempt

# Register your models here.
admin.site.register(Letter)
admin.site.register(ExampleWord)
admin.site.register(Lesson)
admin.site.register(LessonLetter)
admin.site.register(QuizAttempt)
admin.site.register(QuestionAttempt)
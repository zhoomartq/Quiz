from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Quiz(models.Model):
    title = models.CharField(max_length=155)
    description = models.TextField()
    start = models.DateField(auto_now_add=True)
    end = models.DateField()

    def __str__(self):
        return self.title


QUESTION_TYPES = (
    ('text answer', 'text'),
    ('one answer', 'one'),
    ('multiple answer', 'multiple'),
)


class Question(models.Model):
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=80, choices=QUESTION_TYPES)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True, related_name='questions')

    def __str__(self):
        return self.title


class Choice(models.Model):
    title = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text_answer = models.TextField(null=True)
    one_answer = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, related_name='one_answer')
    multiple_answers = models.ManyToManyField(Choice)






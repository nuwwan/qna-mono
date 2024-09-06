from django.db import models
from django.contrib.auth import get_user_model

from user.models import Tag, Subject

AuthUser = get_user_model()


class DifficultyLevels(models.IntegerChoices):
    EASY = 1, "Easy"
    MEDIUM = 2, "Medium"
    HARD = 3, "Hard"


class Question(models.Model):
    title = models.TextField(null=False)
    image = models.CharField(max_length=1000, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="questions"
    )
    difficulty_level = models.IntegerField(
        choices=DifficultyLevels, default=DifficultyLevels.EASY
    )
    tags = models.ManyToManyField(Tag, through="QuestionTag")
    explanation = models.TextField()

    def __str__(self) -> str:
        return self.title


class QuestionTag(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    title = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000, null=True)
    is_correct_answer = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Paper(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.title


class PaperQuestion(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"paper:{self.paper} - question:{self.question}"


class QuestionAttempt(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    assignee = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"question:{self.question} assignee:{self.assignee}"

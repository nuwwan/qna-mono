from django.db import models
from django.contrib.auth import get_user_model


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"


class Education(models.TextChoices):
    NONE = "none", "None"
    SCHOOL = "school", "School"
    COLLEGE = "college", "College"


AuthUser = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=25)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Subject(models.Model):
    title = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=50)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="topics"
    )
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    birth_day = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    country = models.CharField(max_length=25)
    educational_level = models.CharField(max_length=10, default=Education.NONE)
    tags = models.ManyToManyField(Tag)
    subjects = models.ManyToManyField(Subject)
    topics = models.ManyToManyField(Topic)

    def __str__(self) -> str:
        return self.user.first_name

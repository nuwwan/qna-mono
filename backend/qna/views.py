from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuestionSerializer
from .models import Question

#
# Question Views
#


# Create Question
class CreateQuestion(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


# Update Question
class UpdateQuestion:
    pass


# Update answer
class UpdateAnswer:
    pass


# Remove Question
class RemoveQuestion:
    pass


# Get User Questions
class GetUserQuestions(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)


# Get questions for the some tags
class GetTagsQuestions(generics.ListAPIView):
    pass


#
# Review Views
#


# Add a Review to Question
class AddQuestionReview:
    pass


# Like a Review
class LikeReview:
    pass


# Dislike a Review
class DislikeReview:
    pass

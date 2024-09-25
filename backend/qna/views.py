from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuestionSerializer
from .models import Question, QuestionTag

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
class UpdateQuestion(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)


# Remove Question
class RemoveQuestion(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        try:
            # get question
            question = self.get_object()

            # remove question tag
            question_tags = QuestionTag.objects.filter(question=question)
            question_tags.delete()

            # remove question
            self.perform_destroy(question)
            return Response(
                {"message": "Question and related answers deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Http404 as ex:
            return Response(
                {
                    "message": f"The Question specefied by id={kwargs.get('pk')} does not exists"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            return Response(
                {"message": f"Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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


class AddUserQuestion:
    pass

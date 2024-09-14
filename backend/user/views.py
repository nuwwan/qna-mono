from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Profile, Subject, Tag, Topic
from .serializers import (
    ProfileSerializer,
    SubjectSerializer,
    SubjectFilterSerializer,
    TagSerializer,
    TagFilterSerializer,
)


#
# Profile Views
#
class CreateProfile(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class RetieveUpdateProfile(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            raise PermissionDenied("Profile Not Found")


#
# Subject Views
#
class GetSubjects(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = SubjectSerializer

    def get_queryset(self):
        # Validate the query parameters
        filter_serializer = SubjectFilterSerializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        prefix = self.request.query_params.get("title")
        return Subject.objects.filter(title__startswith=prefix)[:8]


class CreateSubject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        title = request.data.get("title")

        if not title or len(title) < 2:
            return Response(
                {
                    "error": "Title is required and length should be two or more characters"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to get the subject, or create it if it doesn't exist
        subject, created = Subject.objects.get_or_create(title=title)

        serializer = SubjectSerializer(subject)

        if created:
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )


#
# Tag Views
#
class CreateTag(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        title = request.data.get("title")

        if not title or len(title) < 2:
            return Response(
                {
                    "error": "Title is required and length should be two or more characters"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        # format the input
        title = title.lower()
        title = title.strip()

        # Try to get the subject, or create it if it doesn't exist
        subject, created = Tag.objects.get_or_create(title=title)

        serializer = TagSerializer(subject)

        if created:
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )


class RemoveTag:
    pass


class GetTags(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = TagSerializer

    def get_queryset(self):
        # Validate the query parameters
        filter_serializer = TagFilterSerializer(data=self.request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        prefix = self.request.query_params.get("title")
        return Tag.objects.filter(title__startswith=prefix)[:8]


#
# Topic Views
#

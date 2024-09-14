from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Profile, Subject, Tag, Topic
from .serializers import ProfileSerializer, SubjectSerializer, SubjectFilterSerializer


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


class RemoveSubject:
    pass


#
# Tag Views
#
class CreateTag:
    pass


class RemoveTag:
    pass


class GetTags:
    pass


#
# Topic Views
#

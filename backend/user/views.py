from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Profile
from .serializers import ProfileSerializer


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


class GetProfileDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                data={"message": "No profile is associated with this user!"},
                status=status.HTTP_404_NOT_FOUND,
            )


class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


"""
Subject Views
"""


class CreateSubject:
    pass


class RemoveSubject:
    pass


class GetSubjects:
    pass


"""
Tag Views
"""


class CreateTag:
    pass


class RemoveTag:
    pass


class GetTags:
    pass

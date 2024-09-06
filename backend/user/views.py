from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.response import Response

"""
Profile Views
"""


class CreateProfile(APIView):
    def post(self, request, *args, **kwargs):
        return Response(data={"message": "successful"}, status=status.HTTP_201_CREATED)


class ProfileDetail(RetrieveUpdateAPIView):
    pass


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

from rest_framework.serializers import ModelSerializer, Serializer, CharField
from .models import Profile, Tag, Subject, Topic


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ["user"]


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "title"]


class SubjectFilterSerializer(Serializer):
    prefix = CharField(required=True, max_length=10, min_length=2)

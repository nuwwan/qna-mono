from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    IntegerField,
)
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
    title = CharField(required=True, max_length=10, min_length=2)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagFilterSerializer(Serializer):
    title = CharField(required=True, max_length=10, min_length=2)


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"


class TopicFilterSerializer(Serializer):
    title = CharField(required=True, max_length=10, min_length=2)
    subject = IntegerField()

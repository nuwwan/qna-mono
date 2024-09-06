from rest_framework.serializers import ModelSerializer
from .models import Profile, Tag, Subject, Topic


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ["user"]

from django.urls import path

from .views import (
    CreateProfile,
    RetieveUpdateProfile,
    GetSubjects,
    CreateSubject,
    CreateTag,
    GetTags,
)

urlpatterns = [
    path("create_profile/", CreateProfile.as_view(), name="create_profile"),
    path("profile_detail/", RetieveUpdateProfile.as_view(), name="profile_detail"),
    path("get_subjects/", GetSubjects.as_view(), name="get_subjects"),
    path("create_subject/", CreateSubject.as_view(), name="create_subject"),
    path("create_tag/", CreateTag.as_view(), name="create_tag"),
    path("get_tags/", GetTags.as_view(), name="get_tags"),
]

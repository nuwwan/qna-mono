from django.urls import path

from .views import CreateProfile, ProfileDetail, GetProfileDetail

urlpatterns = [
    path("create_profile/", CreateProfile.as_view(), name="create_profile"),
    path("profile_detail/", ProfileDetail.as_view(), name="profile_detail"),
    path("get_profile_detail/", GetProfileDetail.as_view(), name="get_profile_detail"),
]

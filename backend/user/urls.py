from django.urls import path

from .views import CreateProfile, RetieveUpdateProfile

urlpatterns = [
    path("create_profile/", CreateProfile.as_view(), name="create_profile"),
    path("profile_detail/", RetieveUpdateProfile.as_view(), name="profile_detail"),
]

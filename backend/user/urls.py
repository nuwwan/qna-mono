from django.urls import path

from .views import CreateProfile

urlpatterns = [
    path("create_profile/", CreateProfile.as_view(), name="create_profile"),
]

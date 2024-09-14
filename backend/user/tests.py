from datetime import date

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware

from rest_framework.test import APITestCase
from rest_framework import status

from authentication.utils import generate_jwt_token

from .models import Profile, Tag, Topic, Subject, Gender, Education

"""
To run tests
python manage.py test user.tests.BaseProfileTest
"""

AuthUser = get_user_model()

sample_user_payload = {"email": "test_user@gmail.com", "password": "test"}


class BaseProfileTest(APITestCase):
    def setUp(self) -> None:
        user = AuthUser.objects.create(
            email=sample_user_payload.get("email"),
            password=sample_user_payload.get("password"),
        )

        # create tags
        tag = Tag.objects.create(title="test")

        # create subject
        subject = Subject.objects.create(title="test_subject")

        # create topics
        topic = Topic.objects.create(title="test_topic", subject=subject)

        birth_date = date(2000, 1, 1)

        sample_profile_payload = {
            "birth_day": birth_date.isoformat(),
            "gender": Gender.MALE,
            "country": "Sri Lanka",
            "educational_level": Education.COLLEGE,
            "tags": [tag.id],
            "subjects": [subject.id],
            "topics": [topic.id],
        }
        self.user = user
        self.token = generate_jwt_token(user)
        self.profile = sample_profile_payload
        return super().setUp()


class CreateProfileTest(BaseProfileTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("create_profile")
        super().__init__(methodName)

    def test_create_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.post(self.url, self.profile, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_with_no_subject(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.post(
            self.url, {**self.profile, "subjects": []}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetProfileTest(BaseProfileTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("profile_detail")
        super().__init__(methodName)

    def test_create_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create a profile
        profile = Profile.objects.create(
            user=self.user,
            birth_day=self.profile.get("birth_day"),
            gender=self.profile.get("gender"),
            country=self.profile.get("country"),
            educational_level=self.profile.get("educational_level"),
        )
        profile.tags.set(
            self.profile.get("tags"),
        )

        profile.subjects.set(
            self.profile.get("subjects"),
        )

        profile.subjects.set(
            self.profile.get("topics"),
        )

        # get profile object
        response = self.client.get(self.url, format="json")

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_has_no_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # get profile object
        response = self.client.get(self.url, format="json")

        # assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UpdateProfileTest(BaseProfileTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("profile_detail")
        super().__init__(methodName)

    def test_update_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create a profile
        profile = Profile.objects.create(
            user=self.user,
            birth_day=self.profile.get("birth_day"),
            gender=self.profile.get("gender"),
            country=self.profile.get("country"),
            educational_level=self.profile.get("educational_level"),
        )
        profile.tags.set(
            self.profile.get("tags"),
        )

        profile.subjects.set(
            self.profile.get("subjects"),
        )

        profile.subjects.set(
            self.profile.get("topics"),
        )

        new_country = "India"

        new_data = {**self.profile, "country": new_country}
        # get profile object
        response = self.client.put(self.url, new_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("country"), new_country)

    def test_patch_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create a profile
        profile = Profile.objects.create(
            user=self.user,
            birth_day=self.profile.get("birth_day"),
            gender=self.profile.get("gender"),
            country=self.profile.get("country"),
            educational_level=self.profile.get("educational_level"),
        )
        profile.tags.set(
            self.profile.get("tags"),
        )

        profile.subjects.set(
            self.profile.get("subjects"),
        )

        profile.subjects.set(
            self.profile.get("topics"),
        )

        new_country = "India"

        new_data = {"country": new_country}
        # get profile object
        response = self.client.patch(self.url, new_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("country"), new_country)

    def test_update_profile_when_no_record_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        new_country = "India"

        new_data = {"country": new_country}
        # get profile object
        response = self.client.patch(self.url, new_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

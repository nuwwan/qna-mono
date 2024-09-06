from datetime import datetime

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware

from rest_framework.test import APITestCase
from rest_framework import status

from authentication.utils import generate_jwt_token

from .models import Profile, Tag, Topic, Subject, Gender, Education

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

        birth_date = make_aware(datetime(2000, 1, 1, 0, 0))

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

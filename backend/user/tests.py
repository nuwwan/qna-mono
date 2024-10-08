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


class GetSubjectTest(BaseProfileTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("get_subjects")
        super().__init__(methodName)

    def test_get_subjects(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create some subjects
        Subject.objects.bulk_create(
            [
                Subject(title="test1"),
                Subject(title="test2"),
                Subject(title="test3"),
                Subject(title="test4"),
                Subject(title="test5"),
                Subject(title="test6"),
                Subject(title="test7"),
                Subject(title="test8"),
                Subject(title="test9"),
                Subject(title="test10"),
            ]
        )

        response = self.client.get(self.url, {"title": "test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)

    def test_when_no_objects(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.get(self.url, {"title": "sama"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_short_prefix(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create some subjects
        Subject.objects.bulk_create(
            [
                Subject(title="test1"),
                Subject(title="test2"),
                Subject(title="test3"),
                Subject(title="test4"),
                Subject(title="test5"),
                Subject(title="test6"),
                Subject(title="test7"),
                Subject(title="test8"),
                Subject(title="test9"),
                Subject(title="test10"),
            ]
        )

        response = self.client.get(self.url, {"title": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateSubjectTest(BaseProfileTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("create_subject")
        super().__init__(methodName)

    def test_create_subjects(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.post(self.url, {"title": "test"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), "test")

    def test_short_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.post(self.url, {"title": "t"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_existing_subject(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create a subject
        subject = Subject.objects.create(title="test")

        response = self.client.post(self.url, {"title": "test"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), subject.id)


class CreateTagTest(BaseProfileTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("create_tag")
        super().__init__(methodName)

    def test_create_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.post(self.url, {"title": "tag"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), "tag")

    def test_short_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.post(self.url, {"title": "t"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_existing_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create a subject
        tag = Tag.objects.create(title="tag")

        response = self.client.post(self.url, {"title": "tag"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), tag.id)

    def test_case_convert(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        title = "Tag"

        response = self.client.post(self.url, {"title": title}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), title.lower())

    def test_tag_with_spaces(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        title = "test tag"

        response = self.client.post(self.url, {"title": title}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), title.strip())


class GetTagsTest(BaseProfileTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("get_tags")
        super().__init__(methodName)

    def test_get_tags(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create some subjects
        Tag.objects.bulk_create(
            [
                Tag(title="test1"),
                Tag(title="test2"),
                Tag(title="test3"),
                Tag(title="test4"),
                Tag(title="test5"),
                Tag(title="test6"),
                Tag(title="test7"),
                Tag(title="test8"),
                Tag(title="test9"),
                Tag(title="test10"),
            ]
        )

        response = self.client.get(self.url, {"title": "test"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)

    def test_when_no_objects(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.get(self.url, {"title": "tag"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_short_prefix(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create some subjects
        Tag.objects.bulk_create(
            [
                Tag(title="test1"),
                Tag(title="test2"),
                Tag(title="test3"),
                Tag(title="test4"),
                Tag(title="test5"),
                Tag(title="test6"),
                Tag(title="test7"),
                Tag(title="test8"),
                Tag(title="test9"),
                Tag(title="test10"),
            ]
        )

        response = self.client.get(self.url, {"title": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateTopicsTest(BaseProfileTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("create_topic")
        super().__init__(methodName)

    def test_create_topic(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create subject
        subject = Subject.objects.create(title="Science")

        payload = {"title": "Bio Science", "subject": subject.id}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_existing_topic(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create subject
        subject = Subject.objects.create(title="Science")

        title = "Bio Science"

        # create topic
        topic = Topic(title=title, subject=subject)
        topic.save()

        payload = {"title": title, "subject": subject.id}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_short_topic(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create subject
        subject = Subject.objects.create(title="Science")

        title = "B"

        payload = {"title": title, "subject": subject.id}

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetTopicsTest(BaseProfileTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("get_topics")
        super().__init__(methodName)

    def test_get_topic(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create subject
        subject = Subject.objects.create(title="Science")

        # create topics
        Topic.objects.bulk_create(
            [
                Topic(title="Topic 1", subject=subject),
                Topic(title="Topic 2", subject=subject),
                Topic(title="Topic 3", subject=subject),
                Topic(title="Topic 4", subject=subject),
                Topic(title="Topic 5", subject=subject),
                Topic(title="Topic 6", subject=subject),
                Topic(title="Topic 7", subject=subject),
                Topic(title="Topic 8", subject=subject),
                Topic(title="Topic 9", subject=subject),
                Topic(title="Topic 10", subject=subject),
            ]
        )

        response = self.client.get(self.url, {"title": "Topic", "subject": subject.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)

    def test_get_topic_for_non_exist_subject(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        non_exist_subject_id = 999

        response = self.client.get(
            self.url, {"title": "Topic", "subject": non_exist_subject_id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

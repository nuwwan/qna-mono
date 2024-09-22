from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from authentication.utils import generate_jwt_token
from .models import DifficultyLevels
from user.models import Tag
from .models import Question, QuestionTag, Answer

AuthUser = get_user_model()

sample_user_payload = {"email": "test_user@gmail.com", "password": "test"}


class BaseQnATest(APITestCase):
    def setUp(self) -> None:
        user = AuthUser.objects.create(**sample_user_payload)
        self.user = user
        self.token = generate_jwt_token(user)

        # create some tags
        tag1 = Tag(title="tag1")
        tag2 = Tag(title="tag2")
        tag3 = Tag(title="tag3")
        self.tag1 = tag1
        self.tag2 = tag2
        self.tag3 = tag3

        return super().setUp()


class CreateQuestionTest(BaseQnATest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("create_question")
        super().__init__(methodName)

    def test_create_question(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        payload = {
            "title": "Test Title",
            "difficulty_level": DifficultyLevels.EASY,
            "tags": [{"title": self.tag1.title}, {"title": self.tag2.title}],
            "explanation": "sample explanation",
            "answers": [{"title": "Answer 1"}, {"title": "Answer 2"}],
        }

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_when_tags_exists(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        # create tags on DB
        self.tag1.save()
        self.tag2.save()

        payload = {
            "title": "Test Title",
            "difficulty_level": DifficultyLevels.EASY,
            "tags": [{"title": self.tag1.title}, {"title": self.tag2.title}],
            "explanation": "sample explanation",
            "answers": [{"title": "Answer 1"}, {"title": "Answer 2"}],
        }

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetUserQuestionsTest(BaseQnATest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("get_user_questions")
        super().__init__(methodName)

    def test_get_user_questions(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_get_questions_for_unauthenticated_users(self):
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateUserQuestions(BaseQnATest):
    def test_update_question(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create question
        question = Question.objects.create(
            title="test",
            difficulty_level=DifficultyLevels.EASY,
            explanation="sample explanation",
            author=self.user,
        )
        self.tag1.save()
        self.tag2.save()
        QuestionTag.objects.create(question=question, tag=self.tag1)
        QuestionTag.objects.create(question=question, tag=self.tag2)
        Answer.objects.create(question=question, title="answer 1")
        Answer.objects.create(question=question, title="answer 2")

        # format url
        self.url = reverse("update_question", kwargs={"pk": question.id})

        updated_name = "Test-edited"

        payload = {
            "title": updated_name,
            "difficulty_level": DifficultyLevels.EASY,
            "tags": [{"title": self.tag1.title}, {"title": self.tag2.title}],
            "explanation": "sample explanation",
            "answers": [{"title": "Answer 1"}, {"title": "Answer 2"}],
        }

        response = self.client.put(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), updated_name)

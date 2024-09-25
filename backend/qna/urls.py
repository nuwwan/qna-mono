from django.urls import path
from .views import CreateQuestion, GetUserQuestions, UpdateQuestion, RemoveQuestion

urlpatterns = [
    path("create_question/", CreateQuestion.as_view(), name="create_question"),
    path("get_user_questions/", GetUserQuestions.as_view(), name="get_user_questions"),
    path("update_question/<int:pk>/", UpdateQuestion.as_view(), name="update_question"),
    path("delete_question/<int:pk>/", RemoveQuestion.as_view(), name="delete_question"),
]

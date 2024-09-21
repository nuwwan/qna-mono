from django.urls import path
from .views import CreateQuestion

urlpatterns = [
    path("create_question/", CreateQuestion.as_view(), name="create_question")
]

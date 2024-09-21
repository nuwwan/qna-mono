from rest_framework import serializers

from .models import Question, Answer, QuestionTag
from user.models import Tag


class TagQuestionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)

    class Meta:
        model = Tag
        fields = ["title"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "title", "image", "is_correct_answer", "created_date"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    tags = TagQuestionSerializer(many=True)

    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ["author"]

    def create(self, validated_data):
        # Get answers
        answers = validated_data.pop("answers")

        # get the tags
        tags = validated_data.pop("tags")

        # Save the answer
        question = Question.objects.create(**validated_data)

        # create the tags
        for tag_data in tags:
            tag, created = Tag.objects.get_or_create(title=tag_data["title"])
            QuestionTag.objects.create(question=question, tag=tag)

        # create the answers
        for answer in answers:
            Answer.objects.create(question=question, **answer)

        return question

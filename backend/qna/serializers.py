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

    def update(self, instance, validated_data):
        answers_data = validated_data.pop("answers")
        tags_data = validated_data.pop("tags")

        # Update the question title
        instance.title = validated_data.get("title", instance.title)
        instance.image = validated_data.get("image", instance.image)
        instance.difficulty_level = validated_data.get(
            "difficulty_level", instance.difficulty_level
        )
        instance.save()

        # Update tags
        instance.tags.clear()  # Remove existing tags
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(title=tag_data["title"])
            QuestionTag.objects.get_or_create(
                question=instance, tag=tag
            )  # Ensure relation exists

        # Update answers
        instance.answers.all().delete()  # Remove all existing answers for simplicity
        for answer_data in answers_data:
            Answer.objects.create(question=instance, **answer_data)
        return instance

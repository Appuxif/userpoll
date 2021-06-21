from rest_framework import serializers

from mainapp.models import (
    Poll,
    Question,
    MemberAnswer,
    Member,
)


class QuestionSetSerializer(serializers.ModelSerializer):
    """Сериалайзер списка вопросов для опроса"""

    class Meta:
        model = Question
        fields = (
            'pk',
            'kind',
            'text',
        )


class PollSerializer(serializers.ModelSerializer):
    """Сериалайзер опросов"""

    question_set = QuestionSetSerializer(
        label='Список вопросов',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Poll
        fields = (
            'pk',
            'name',
            'desc',
            'question_set',
            'date_started',
            'date_ended',
        )


class MemberSerializer(serializers.ModelSerializer):
    """Сериалайзер для участника опроса"""

    class Meta:
        model = Member
        fields = (
            'member_id',
        )


class MemberAnswerSerializer(serializers.ModelSerializer):
    """Сериалайзер ответа на вопрос опроса"""

    member = serializers.CharField(
        label='Участник опроса',
        help_text='Участник опроса',
        source='member.member_id',
    )

    class Meta:
        model = MemberAnswer
        fields = (
            'pk',
            'value',
            'question',
            'member',
        )

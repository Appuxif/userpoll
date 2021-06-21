import django_filters

from mainapp.models import (
    Question,
    Poll,
)


class PollFilterSet(django_filters.FilterSet):
    """Фильтры для списка опросов"""

    member_id = django_filters.CharFilter(
        label='Участник опроса',
        help_text='Поиск опросов, в которых принимает участие member_id',
        field_name='question__memberanswer__member__member_id',
        distinct=True,
    )


class MemberAnswerFilterSet(django_filters.FilterSet):
    """Фильтры для списка ответов участника"""
    member_id = django_filters.CharFilter(
        label='Участник опроса',
        help_text='Поиск ответов участника',
        field_name='member__member_id',
        distinct=True,
    )

    question_id = django_filters.ModelChoiceFilter(
        label='Вопрос ответа',
        help_text='Поиск ответов участника по конкретному вопросу',
        queryset=Question.objects.all(),
    )

    poll_id = django_filters.ModelChoiceFilter(
        label='Опрос ответа',
        help_text='Поиск ответов участника по конкретному опросу',
        queryset=Poll.objects.all(),
        field_name='question__poll',
    )

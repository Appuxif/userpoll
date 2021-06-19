from django.contrib.auth.models import User
from django.db import models


class Member(models.Model):
    """Участник"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        help_text='Можно оставить пустым',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    member_id = models.CharField(
        verbose_name='Уникальный идентификатор',
        help_text='Максимум символов: 32',
        max_length=32,
        unique=True,
    )

    def __str__(self):
        return f'{self.pk} - {self.member_id} - {self.user}'


class Poll(models.Model):
    """Опрос"""

    name = models.CharField(
        verbose_name='Название',
        help_text='Максимум символов: 64',
        max_length=64,
    )
    desc = models.TextField(
        verbose_name='Описание',
        help_text='Максимум символов: 256',
        max_length=256,
    )
    members = models.ManyToManyField(
        Member,
        verbose_name='Участники опроса',
        help_text='Список участников, которые дают ответы на опрос или уже окончили опрос',
        blank=True,
    )
    date_started = models.DateTimeField(
        verbose_name='Дата старта',
        help_text='Устанавливается при создании автоматически',
        auto_now_add=True,
    )
    date_ended = models.DateTimeField(
        verbose_name='Дата окончания',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.pk} - {self.name}'


class Question(models.Model):
    """Вопрос"""

    KIND_DEFAULT = 'text'
    KIND_CHOICES = (
        (KIND_DEFAULT, 'Ответ текстом'),
        ('one', 'Ответ с выбором одного варианта'),
        ('many', 'Ответ с выбором нескольких вариантов'),
    )
    kind = models.CharField(
        verbose_name='Тип вопроса',
        max_length=8,
        choices=KIND_CHOICES,
        default=KIND_DEFAULT,
        db_index=True,
    )
    text = models.TextField(
        verbose_name='Текст вопроса',
        help_text='Максимум символов: 1024',
        max_length=1024,
    )
    poll = models.ForeignKey(
        Poll,
        verbose_name='Опрос',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.pk} - {self.kind} - {self.poll.name}'


class MemberAnswer(models.Model):
    """Ответ участника на вопрос опроса"""

    value = models.CharField(
        verbose_name='Значение ответа',
        help_text='Максимум символов: 128',
        max_length=128,
    )
    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
    )
    member = models.ForeignKey(
        Member,
        verbose_name='Участник опроса',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return (
            f'{self.pk} - '
            f'{self.value} - '
            f'{self.question.kind} - '
            f'{self.question.poll.name} - '
            f'{self.member.member_id}'
        )

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from mainapp.models import (
    MemberAnswer,
    Poll,
)


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=MemberAnswer)
def post_save_member_answer(sender, instance: MemberAnswer, created, **kwargs):
    # Присоединяем участника к опросу, если это его первый ответ
    poll = Poll.objects.get(question__memberanswer=instance)
    poll.members.add(instance.member)

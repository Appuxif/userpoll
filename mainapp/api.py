from django.contrib.auth.models import AnonymousUser
from rest_framework import (
    viewsets,
    mixins,
    permissions,
)

from mainapp.filters import (
    PollFilterSet,
    MemberAnswerFilterSet,
)
from mainapp.models import (
    Poll,
    MemberAnswer,
    Member,
)
from mainapp.serializers import (
    PollSerializer,
    MemberAnswerSerializer,
)


class PollAPIView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API списка активных опросов
    """

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = Poll.objects.filter(date_ended__isnull=True)
    serializer_class = PollSerializer
    filterset_class = PollFilterSet


class MemberAnswerAPIView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    API ответа на вопрос опроса
    """

    permission_classes = [
        permissions.AllowAny,
    ]
    queryset = MemberAnswer.objects.all()
    serializer_class = MemberAnswerSerializer
    filterset_class = MemberAnswerFilterSet

    def perform_create(self, serializer: MemberAnswerSerializer):

        # Создаем участника если его нет
        user = self.request.user
        member_id = serializer.validated_data['member']['member_id']
        if isinstance(user, AnonymousUser):
            user = None

        member, created = Member.objects.get_or_create(
            member_id=member_id,
            user=user,
        )

        serializer.save(member=member)

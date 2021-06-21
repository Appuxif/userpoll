from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from mainapp.models import (
    Poll,
    Member,
    MemberAnswer,
)
from mainapp.serializers import (
    PollSerializer,
    MemberAnswerSerializer,
)


class TestUserTokenAuth(APITestCase):
    """Тесты авторизации"""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            'testuser',
            'testuser@example.com',
            'testuserpwd',
        )

    def test_token_auth(self):
        """Тест получения токена через API"""
        response = self.client.post(
            '/api/v1/token/auth/',
            {
                'username': 'testuser',
                'password': 'testuserpwd',
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = Token.objects.get(user__username='testuser')
        self.assertEqual(response.data['token'], token.key)


class TestPollAPI(APITestCase):
    """Тесты опросов"""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            'testuser',
            'testuser@example.com',
            'testuserpwd',
        )

        for i in range(10):
            p = Poll.objects.create(
                name=f'test_name_{i}',
                desc=f'test_desc_{i}',
            )

        # Создание вопроса в последнем опросе
        question = p.question_set.create(
            text='test question text',
        )

        # Создание участника опроса
        member = Member.objects.create(
            member_id='111',
        )

        # Создание ответа от участника
        question.memberanswer_set.create(
            value='123',
            member=member,
        )

    def setUp(self) -> None:
        self.client.force_authenticate(User.objects.get(username='testuser'))

    def test_poll_list_serializer(self):
        """
        Тест сериалайзера для списка опросов
        """

        # Запрос списка опросов
        polls = Poll.objects.all()

        # Получение сериализованных данных
        serializer = PollSerializer(
            polls,
            many=True,
        )

        # Проверка сериализованных данных
        self.assertEqual(len(serializer.data), polls.count())

        fields = (
            'pk',
            'name',
            'desc',
            'question_set',
            'date_started',
            'date_ended',
        )
        for field in fields:
            self.assertIn(field, serializer.data[0])

    def test_poll_serializer_with_questions(self):
        """
        Тест сериалайзера для опроса со списком вопросов
        """

        # Получение последнего опроса из сетапа
        poll = Poll.objects.get(name='test_name_9')

        # Получение сериализованных данных
        serializer = PollSerializer(poll)

        # Проверка сериализованных данных
        self.assertEqual(len(serializer.data['question_set']), poll.question_set.count())
        fields = (
            'pk',
            'kind',
            'text',
        )
        for field in fields:
            self.assertIn(field, serializer.data['question_set'][0])

    def test_poll_list(self):
        """
        Тест списка активных опросов
        """

        response = self.client.get('/api/v1/polls/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        polls = Poll.objects.all()

        serializer = PollSerializer(
            polls,
            many=True,
        )
        self.assertEqual(response.data['results'], serializer.data)

    def test_poll_list_by_member_id(self):
        """
        Тест списка активных опросов. Фильтр по участнику
        """

        response = self.client.get('/api/v1/polls/?member_id=111')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        polls = Poll.objects.filter(question__memberanswer__member__member_id=111)

        serializer = PollSerializer(
            polls,
            many=True,
        )
        self.assertEqual(response.data['results'], serializer.data)

    def test_poll_list_guest(self):
        """
        Тест списка активных опросов.
        Неавторизованный
        """
        self.client.logout()
        self.test_poll_list()
        self.test_poll_list_by_member_id()

    def test_member_answer_serializer(self):
        """Тест сериалайзера ответа на вопрос опроса"""

        # Получение последнего опроса из сетапа
        poll = Poll.objects.get(name='test_name_9')

        # Получение вопроса опроса
        question = poll.question_set.first()

        # Создание участника опроса
        member = Member.objects.create(
            member_id='112',
        )

        # Создание ответа на вопрос
        answer = question.memberanswer_set.create(
            value='123',
            member=member,
        )

        # Получение сериализованных данных
        serializer = MemberAnswerSerializer(answer)

        # Проверка сериализованных данных
        self.assertEqual(serializer.data['pk'], answer.pk)
        self.assertEqual(serializer.data['value'], '123')
        self.assertEqual(serializer.data['question'], question.pk)
        self.assertEqual(serializer.data['member'], '112')

    def test_answer_poll_question(self):
        """Тест ответа на вопрос опроса"""

        # Получение последнего опроса из сетапа
        poll = Poll.objects.get(name='test_name_9')

        # Производим ответ на каждый вопрос опроса
        for question in poll.question_set.all():
            response = self.client.post(
                '/api/v1/answers/',
                {
                    'value': 'test value',
                    'question': question.pk,
                    'member': 123,
                },
                # format='json',
            )

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            answer = MemberAnswer.objects.get(pk=response.data['pk'])

            serializer = MemberAnswerSerializer(answer)

            self.assertEqual(response.data, serializer.data)

    def test_answer_poll_question_guest(self):
        """
        Тест ответа на вопрос опроса. Неавторизованный
        """
        self.client.logout()
        self.test_answer_poll_question()

    def test_answer_list(self):
        """Тест списка ответов участника"""

        response = self.client.get(
            '/api/v1/answers/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answers = MemberAnswer.objects.all()
        serializer = MemberAnswerSerializer(answers, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_answer_list_by_member_id(self):
        """Тест списка ответов участника. Фильтр по участнику"""

        response = self.client.get(
            '/api/v1/answers/?member_id=111'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answers = MemberAnswer.objects.filter(member__member_id=111)
        serializer = MemberAnswerSerializer(answers, many=True)
        self.assertEqual(response.data['results'], serializer.data)

        # Несуществующий участник
        response = self.client.get(
            '/api/v1/answers/?member_id=999'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answers = MemberAnswer.objects.none()
        serializer = MemberAnswerSerializer(answers, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_answer_list_by_question_id(self):
        """Тест списка ответов участника. Фильтр по вопросу"""

        question = MemberAnswer.objects.first().question

        response = self.client.get(
            f'/api/v1/answers/?question_id={question.pk}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answers = MemberAnswer.objects.filter(question__pk=question.pk)
        serializer = MemberAnswerSerializer(answers, many=True)
        self.assertEqual(response.data['results'], serializer.data)

        # Несуществующий вопрос
        response = self.client.get(
            '/api/v1/answers/?question_id=9999'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_list_by_poll_id(self):
        """Тест списка ответов участника. Фильтр по опросу"""

        poll = MemberAnswer.objects.first().question.poll

        response = self.client.get(
            f'/api/v1/answers/?poll_id={poll.pk}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answers = MemberAnswer.objects.filter(question__poll__pk=poll.pk)
        serializer = MemberAnswerSerializer(answers, many=True)
        self.assertEqual(response.data['results'], serializer.data)

        # Несуществующий опрос
        response = self.client.get(
            '/api/v1/answers/?poll_id=9999'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_list_guest(self):
        """
        Тест списка ответов участника. Неавторизованный
        """

        self.client.logout()
        self.test_answer_list()
        self.test_answer_list_by_member_id()
        self.test_answer_list_by_question_id()
        self.test_answer_list_by_poll_id()

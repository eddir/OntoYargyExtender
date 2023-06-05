from contextlib import suppress

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from panel.serializers import UserSerializer
from panel.utils import api_response

from authentication.models import Request


class UsersView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        """Список текущих пользователей"""
        users = []

        # select only active users
        for user in get_user_model().objects.filter(is_active=True):
            users.append({
                "user_id": user.id,
                "username": user.username,
                "name": user.first_name + " " + user.last_name,
                "email": user.email,
                # todo: группа (роль) пользователя - owner, admin
            })

        return api_response(users)

class UserCreateView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return api_response("Пользователь добавлен.")


class UserRemoveView(DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return api_response("Пользователь удалён.")


class RequestsView(APIView):

    @method_decorator(login_required)
    @staticmethod
    def get(request):
        """Список запросов на регистрацию"""
        requests = []

        for request in Request.objects.all():
            requests.append({
                "request_id": request.id,
                "username": request.user.username,
                "name": request.user.first_name + " " + request.user.last_name,
                "email": request.user.email,
                "organization": request.organization,
                "position": request.position,
                "goal": request.goal,
            })

        return api_response(requests)

class RequestView(APIView):

    @method_decorator(login_required)
    @staticmethod
    def post(request, pk):
        """Одобрить запрос на регистрацию"""
        request = Request.objects.get(pk=pk)
        user = User.objects.get(pk=request.user.id)
        user.is_active = True
        user.save()
        request.delete()

        message = """Здравствуйте, {0}!

Ваш запрос на регистрацию в системе "OntologyFiller" одобрен.

Логин: {1}
Пароль: {2}

С уважением, администрация системы "OntologyFiller".
""".format(user.first_name, user.username, user.password)

        sent = False
        with suppress(Exception):
            user.email_user("Запрос одобрен", message)
            sent = True

        return api_response("Запрос одобрен.") if sent else api_response("Запрос одобрен, но письмо не отправлено. "
                                                                         "Проверьте настройки сервера.")

    @method_decorator(login_required)
    @staticmethod
    def delete(request, pk):
        """Отклонить запрос на регистрацию"""
        request = Request.objects.get(pk=pk)
        request.delete()
        return api_response("Запрос отклонён.")


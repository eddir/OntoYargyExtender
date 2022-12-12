from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from panel.serializers import UserSerializer
from panel.utils import api_response


class UsersView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        """Список текущих пользователей"""
        users = []

        for user in get_user_model().objects.all():
            users.append({
                "user_id": user.id,
                "username": user.username,
                "name": user.first_name + " " + user.last_name,
                "email": user.email,
                # todo: группа (роль) пользователя - owner, admin
            })

        return api_response(users)


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return api_response("Пользователь добавлен.")


class UserRemoveView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return api_response("Пользователь удалён.")


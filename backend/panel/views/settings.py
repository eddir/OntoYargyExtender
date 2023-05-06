from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from panel.utils import api_response


class VersionView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        """Версия панели, Watchdog и базы данных MySQL"""
        return api_response("1.1.0")


class PingView(APIView):

    @staticmethod
    def get(request):
        return api_response("Pong")

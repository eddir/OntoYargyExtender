from django.contrib.auth import authenticate, get_user_model
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from panel.exceptions import AUTH_FAILED, APIError, RESPONSE_OK, AUTH_WRONG_REFRESH_TOKEN, UNEXPECTED_ERROR, \
    AUTH_WRONG_CREDENTIALS

from authentication.models import Request


@csrf_exempt
@api_view(('POST',))
@authentication_classes([])
@permission_classes([])
def token_refresh(request):
    if "JWT-REFRESH" not in request.COOKIES:
        raise APIError(AUTH_WRONG_REFRESH_TOKEN, "Токен просрочен")

    serializer = TokenRefreshSerializer(data={"refresh": request.COOKIES["JWT-REFRESH"]})
    serializer.is_valid(raise_exception=True)
    return jwt(request, serializer.validated_data['access'], serializer.validated_data['refresh'])


@csrf_exempt
@api_view(('POST',))
@authentication_classes([])
@permission_classes([])
def auth(request):
    request.user = authenticate(username=request.data['login'], password=request.data['password'])
    if request.user is not None:
        return login(request)
    else:
        raise APIError(AUTH_WRONG_CREDENTIALS)


@api_view(('POST',))
@authentication_classes([])
@permission_classes([])
def register(request):
    if get_user_model().objects.filter(username=request.data['username']).exists():
        raise APIError(message="Пользователь с таким логином уже существует.")

    user = get_user_model().objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email'],
        is_active=False
    )
    user.save()

    registration_request = Request()
    registration_request.user = user
    registration_request.organization = request.data['organization']
    registration_request.position = request.data['position']
    registration_request.goal = request.data['goal']
    registration_request.save()

    return Response(
        {
            "code": RESPONSE_OK,
            "response": {
                "message": "Регистрация прошла успешно."
            }
        }
    )


@api_view(('POST',))
@authentication_classes([])
@permission_classes([])
def logout(request):
    response = Response(
        {
            "code": RESPONSE_OK,
            "response": {
                "message": "Выход выполнен."
            }
        }
    )
    response.set_cookie("JWT", "", max_age=0, httponly=True, samesite="None", secure=True)
    response.set_cookie("JWT-REFRESH", "", max_age=0, httponly=True, samesite="None", secure=True, path="/auth")
    return response


def login(request):
    token = RefreshToken.for_user(request.user)
    return jwt(request, token.access_token, token)


def jwt(request, access_token, refresh_token):
    response = Response(
        {
            "code": RESPONSE_OK,
            "response": {
                "message": "Авторизация пройдена.",
                "csrf": str(csrf(request)['csrf_token'])
            }
        }
    )

    response.set_cookie("JWT", str(access_token), max_age=3600 * 24 * 14, httponly=True, samesite="None",
                        secure=True)
    response.set_cookie("JWT-REFRESH", str(refresh_token), max_age=3600 * 24 * 14, httponly=True, samesite="None",
                        secure=True, path="/auth")
    return response

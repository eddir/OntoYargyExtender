from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.views import auth, token_refresh, register, logout

urlpatterns = [
    path('credentials/login/', auth),
    path('credentials/register/', register),
    path('credentials/logout/', logout),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', token_refresh, name='token_refresh'),
]

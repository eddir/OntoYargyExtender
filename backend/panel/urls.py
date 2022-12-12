from django.urls import path

from .views.ontologies import OntologyView, OntologyTasksView, OntologyDownloadView
from .views.settings import VersionView, PingView
from .views.users import UsersView, UserCreateView, UserRemoveView
from .views.webhook import WebhookPush

app_name = 'panel'

urlpatterns = [

    # GitHub webhooks

    path('webhook/', WebhookPush.as_view()),

    # API

    path('api/', UsersView.as_view()),

    path('api/version/', VersionView.as_view()),
    path('api/ping/', PingView.as_view()),

    path('api/users/', UsersView.as_view()),
    path('api/users/create/', UserCreateView.as_view()),
    path('api/users/<int:pk>/remove/', UserRemoveView.as_view()),

    path('api/ontologies/', OntologyView.as_view()),
    path('api/ontologies/import/', OntologyView.as_view()),
    path('api/ontologies/tasks/', OntologyTasksView.as_view()),
    path('api/ontologies/<int:pk>/download/', OntologyDownloadView.as_view())
]

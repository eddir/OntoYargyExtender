from django.urls import path

from .views.ontologies import OntologyView, OntologyTasksView, OntologyDownloadView, OntologyFillView, \
    OntologyFillDownloadView
from .views.settings import VersionView, PingView
from .views.users import UsersView, UserCreateView, UserRemoveView, RequestsView, RequestView
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

    path('api/requests/', RequestsView.as_view()),
    path('api/request/<int:pk>/', RequestView.as_view()),

    path('api/requests/', RequestsView.as_view()),

    path('api/ontologies/', OntologyView.as_view()),
    path('api/ontologies/import/', OntologyView.as_view()),
    path('api/ontologies/tasks/', OntologyTasksView.as_view()),
    path('api/ontologies/<int:pk>/download/', OntologyDownloadView.as_view()),
    path('api/ontologies/fill/', OntologyFillView.as_view()),
    path('api/ontologies/fill/<int:pl>/download/', OntologyFillDownloadView.as_view()),

]

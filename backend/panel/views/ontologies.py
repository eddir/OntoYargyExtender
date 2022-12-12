from django.http import HttpResponse
from rest_framework.views import APIView
from django_celery_results.models import TaskResult

from panel.models import Ontology
from panel.utils import api_response
from panel.tasks.ontologies_tasks import import_ontology_task


class OntologyView(APIView):

    @staticmethod
    def get(request):
        return api_response([{
            "id": onto.id,
            "name": onto.name,
        } for onto in Ontology.objects.all()])

    @staticmethod
    def post(request):
        name = request.data['name']
        parser = request.data['parser']
        url = request.data['url']
        task = import_ontology_task.delay(parser, url, name)
        return api_response(task.id + str(parser) + "lfi0")


class OntologyTasksView(APIView):

    @staticmethod
    def get(request):
        return api_response([{
            "id": task.task_id,
            "name": task.task_name,
            "status": task.status,
            "date_created": task.date_created
        } for task in TaskResult.objects.all()])


class OntologyDownloadView(APIView):

    @staticmethod
    def get(request, pk):
        filename = "museum-ontology.owl"
        content = Ontology.objects.get(pk=pk).owl
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response

# project/tasks/sample_tasks.py
from celery import shared_task

from panel.parsers.rad.rad3_parser import RAD3


@shared_task
def import_ontology_task(parser, url, name):

    if parser == "RAD1":
        RAD3(url).process(name)
        return True

    return False


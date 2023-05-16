from django.db import models


class Ontology(models.Model):
    name = models.CharField('Ontology name', max_length=128)
    owl = models.TextField(null=True, blank=True, default=None)


class FilledOntology(models.Model):
    name = models.CharField('Ontology name', max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    owl = models.FileField(upload_to='owl/', null=True, blank=True, default=None)
    text = models.FileField(upload_to='texts/', null=True, blank=True, default=None)
    facts = models.FileField(upload_to='facts/', null=True, blank=True, default=None)
    result = models.FileField(upload_to='owl_filled/', null=True, blank=True, default=None)
    status = models.CharField('Status', max_length=128, default='pending')

from django.db import models


class Ontology(models.Model):
    name = models.CharField('Ontology name', max_length=128)
    owl = models.TextField(null=True, blank=True, default=None)


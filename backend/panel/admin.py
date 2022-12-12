from django.contrib import admin

from panel.models import Ontology


@admin.register(Ontology)
class OntologyAdmin(admin.ModelAdmin):
    pass

from funowl import Ontology, NamedIndividual, OntologyDocument, ClassAssertion, DataPropertyAssertion, Literal, \
    ObjectPropertyAssertion
from rdflib import Namespace, RDFS

MU = Namespace("http://example.org/museum#")
DC = Namespace("http://dublincore.org/2008/01/14/dcelements.rdf")

o = Ontology(MU.singletonText)
o.imports(DC.singletonText)

o.annotation(RDFS.label, "Museum ontology")

o.declarations(NamedIndividual(MU['BobDylan']))
o.declarations(NamedIndividual(MU.Painting1))

o.axioms.append(ClassAssertion(MU.MediaResource, MU.Painting1))
o.axioms.append(ClassAssertion(MU.Agent, MU['BobDylan']))
o.axioms.append(DataPropertyAssertion(MU.title, MU.Painting1,  Literal('знаешь как я соскучился')))
o.axioms.append(DataPropertyAssertion(MU.title, MU['BobDylan'],  Literal('Иванофф')))
o.axioms.append(ObjectPropertyAssertion(MU.hasCreated, MU['BobDylan'],  MU.Painting1))


doc = OntologyDocument(MU, o)
print(str(doc))

"""
Declaration(NamedIndividual(<http://www.semanticweb.org/ontomuseum/museum#Венера, оплакивающая смерть Адониса>))
ClassAssertion(<http://www.semanticweb.org/ontomuseum/museum#artifact> <http://www.semanticweb.org/ontomuseum/museum#Венера, оплакивающая смерть Адониса>)
DataPropertyAssertion(<http://www.semanticweb.org/ontomuseum/museum#author> <http://www.semanticweb.org/ontomuseum/museum#Венера, оплакивающая смерть Адониса> <http://www.semanticweb.org/ontomuseum/museum#Виллебортс Босхарт Томас>)
            """
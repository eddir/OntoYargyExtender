import requests
from bs4 import BeautifulSoup
from funowl import Ontology, NamedIndividual, OntologyDocument, ClassAssertion, DataPropertyAssertion, Literal, \
    ObjectPropertyAssertion
from rdflib import Namespace, RDFS

from panel.models import Ontology as OntologyModel


class RAD3:
    url: ''
    min_id = 3786  # 3786
    max_id = 4000  # 50618

    MU = Namespace("http://example.org/museum#")
    DC = Namespace("http://dublincore.org/2008/01/14/dcelements.rdf")

    ontology = None

    def __init__(self, url):
        self.url = url

    def process(self, name):

        self.ontology = Ontology(self.MU)
        self.ontology.imports(self.DC)
        self.ontology.annotation(RDFS.label, "Museum ontology")

        self.ontology.annotation(RDFS.label, "Museum ontology")

        # self.ontology = """
        # Prefix(owl:=<http://www.w3.org/2002/07/owl#>)
        # Prefix(rdf:=<http://www.w3.org/1999/02/22-rdf-syntax-ns#>)
        # Prefix(xml:=<http://www.w3.org/XML/1998/namespace>)
        # Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)
        # Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)
        #
        # Ontology(<http://www.semanticweb.org/ontomuseum/museum/>
        #
        # Declaration(Class(<http://www.semanticweb.org/ontomuseum/museum/#artifact>))
        # Declaration(Class(<http://www.semanticweb.org/ontomuseum/museum/#person>))
        #
        # Declaration(DataProperty(<http://www.semanticweb.org/ontomuseum/museum/#author>))
        # Declaration(DataProperty(<http://www.semanticweb.org/ontomuseum/museum/#created_at>))
        #
        # SubDataPropertyOf(<http://www.semanticweb.org/ontomuseum/museum/#created_at> owl:topDataProperty)
        # """
        # self.parse()
        # self.ontology += ")"
        #

        self.parse()

        onto = OntologyModel()
        onto.name = name
        onto.owl = OntologyDocument(self.MU, self.ontology)
        onto.save()

    def parse(self):
        """
        1. loop throw all ids from 1 to 3600
        2. parse each page, retrieve information
        3. retrieve incoming by Yargy parser
        4. save knowledge into ontology
        """
        for artifact_id in range(self.min_id, self.max_id):
            print("\n" + str(artifact_id), end="")
            page = requests.get(self.url + str(artifact_id))

            if page.status_code == 200:
                content = page.text
                soup = BeautifulSoup(content, "html.parser")

                artifact_table = soup.find(id='ptabi')

                if artifact_table:
                    author_div = artifact_table.select_one('.aname')
                    author_name_div = author_div.select_one('a')
                    place_div = author_div.select_one('nobr')

                    author_dates = ""
                    author_name = ""
                    place = ""

                    if author_name_div:
                        author_name = author_name_div.text
                        author_div.select_one('a').extract()
                        author_dates = author_div.text.strip()

                    if place_div:
                        place = place_div.next_sibling

                    self.insert({
                        'author_name': author_name,
                        'author_birthdate': author_dates,
                        'place': place,
                        'name': artifact_table.select_one('.pname').text,
                        'date': artifact_table.select_one('.pdate').text,
                        'tech': artifact_table.select_one('.ptech').text,
                        'incoming': " ".join(
                            [el.text for el in artifact_table.select_one('.pcomm').find_next_siblings()]),
                        'artifact_id': str(artifact_id),
                    })
                else:
                    print(" - empty", end="")
            else:
                print(" - %d [%s]" % (page.status_code, self.url + str(artifact_id)), end="")

    def insert(self, data):
        author = data['author_name'].replace(' ', '_')
        name = data['name'].replace(' ', '_')
        base_url = "http://www.semanticweb.org/ontomuseum/museum"

        self.ontology.declarations(NamedIndividual(self.MU['artifact'+data['artifact_id']]))
        self.ontology.declarations(NamedIndividual(self.MU['author'+data['artifact_id']]))

        self.ontology.axioms.append(ClassAssertion(
            self.MU.MediaResource,
            self.MU['artifact'+data['artifact_id']]))
        self.ontology.axioms.append(ClassAssertion(
            self.MU.Agent,
            self.MU['author'+data['artifact_id']]))
        self.ontology.axioms.append(DataPropertyAssertion(
            self.MU.title,
            self.MU['artifact'+data['artifact_id']],
            Literal(name)))
        self.ontology.axioms.append(DataPropertyAssertion(
            self.MU.title,
            self.MU['author'+data['artifact_id']],
            Literal(data['author_name'])))
        self.ontology.axioms.append(ObjectPropertyAssertion(
            self.MU.hasCreated,
            self.MU['author'+data['artifact_id']],
            self.MU['artifact'+data['artifact_id']]))
        self.ontology.axioms.append(DataPropertyAssertion(
            self.MU.creation_date,
            self.MU['artifact'+data['artifact_id']],
            Literal(data['date'])))
        self.ontology.axioms.append(DataPropertyAssertion(
            self.MU.locationName,
            self.MU['artifact'+data['artifact_id']],
            Literal(data['place'])))


if __name__ == "__main__":
    RAD3("http://artkatalog.radmuseumart.ru/ru/").process()

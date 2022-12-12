from typing import overload, Union


class OntologyDeclaration:
    def as_owl(self, onto_type, base_url, name):
        return f'''
Declaration({onto_type}(<{base_url}#{name}>))'''


class OntologyClass(OntologyDeclaration):
    name = ""

    def __init__(self, name):
        self.name = name

    def as_owl(self, base_url, *args, **kwargs):
        return super().as_owl("Class", base_url, self.name)


class OntologyDataProperty(OntologyDeclaration):
    name = ""
    sub_property_of_list = []

    def __init__(self, name):
        self.name = name

    def sub_property_of(self, item):
        self.sub_property_of_list.append(item)

    def as_owl(self, base_url, *args, **kwargs):
        return super().as_owl("DataProperty", base_url, self.name) + "\n".join([
            f'''
SubDataPropertyOf(<{base_url}#{self.name}> owl:{item})\n''' for item in self.sub_property_of_list
        ])


class OntologyNamedIndividual(OntologyDeclaration):
    name = ""

    def __init__(self, name):
        self.name = name

    def as_owl(self, base_url, *args, **kwargs):
        return super().as_owl("NamedIndividual", base_url, self.name)


class OntologyAssertion:
    def as_owl(self, base_url, name1, name2):
        return f'''
ClassAssertion(<{base_url}#{name1} {base_url}#{name2}>))'''


class OntologyClassAssertion(OntologyAssertion):
    onto_class = OntologyClass
    onto_individual = OntologyNamedIndividual

    def __init__(self, onto_class, onto_individual):
        self.onto_class = onto_class
        self.onto_individual = onto_individual

    def as_owl(self, base_url, *args, **kwargs):
        return super().as_owl(base_url, self.onto_class, self.onto_individual)


class OntologyF:
    name = ""
    base_url = "http://www.semanticweb.org/ontomuseum/"

    classes = []
    data_properties = []
    declarations = []
    assertions = []

    def __init__(self, name="museum"):
        self.name = name

    @overload
    def declaration(self, onto_class: Union[OntologyClass, OntologyDeclaration]):
        if onto_class not in self.classes:
            self.classes.append(onto_class)

    def declaration(self, onto_data_property: OntologyDataProperty):
        if onto_data_property not in self.data_properties:
            self.classes.append(onto_data_property)

    def assertion(self, onto_assertion: OntologyAssertion):
        if onto_assertion not in self.assertions:
            self.assertions.append(onto_assertion)

    def as_owl(self):
        owl = f'''
Prefix(owl:=<http://www.w3.org/2002/07/owl#>)
Prefix(rdf:=<http://www.w3.org/1999/02/22-rdf-syntax-ns#>)
Prefix(xml:=<http://www.w3.org/XML/1998/namespace>)
Prefix(xsd:=<http://www.w3.org/2001/XMLSchema#>)
Prefix(rdfs:=<http://www.w3.org/2000/01/rdf-schema#>)

Ontology(<{self.base_url}{self.name}/>'''

        for item in self.classes + self.data_properties:
            owl += item.as_owl(self.base_url + self.name)

        return owl


if __name__ == "__main__":
    onto = Ontology("himan")

    onto_prop = OntologyDataProperty("Course")
    onto_class_student = OntologyClass("Student")
    onto_class_group = OntologyClass("Group")
    onto_ivan = OntologyNamedIndividual("Иван")
    onto_lena = OntologyNamedIndividual("Лена")

    onto.declaration(onto_class_student)
    onto.declaration(onto_class_group)


    onto_prop.sub_property_of("topDataProperty")
    onto.declaration(onto_prop)
    onto.declaration(OntologyDataProperty("YearsOfStudy"))
    onto.assertion(OntologyClassAssertion(onto_class_student, onto_ivan))
    onto.assertion(OntologyClassAssertion(onto_class_student, onto_lena))

    print(onto.as_owl())


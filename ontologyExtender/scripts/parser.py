# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from natasha import NamesExtractor, MorphVocab
from natasha.grammars.addr import INT
from yargy import Parser, rule, not_, or_
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy.predicates import eq
from yargy.predicates import (
    in_, normalized,
    dictionary, )
from yargy.tokenizer import (
    QUOTES
)

from ontology import OntoFacts


class TooManyStates(Exception): pass


def capped(method):
    def wrap(self, column, *args):
        before = len(column.states)
        method(self, column, *args)
        after = len(column.states)

        self.states += (after - before)
        if self.cap and self.states > self.cap:
            raise TooManyStates

    return wrap


class CappedParser(Parser):
    def reset(self):
        self.states = 0

    def __init__(self, *args, cap=None, **kwargs):
        self.states = None
        self.cap = cap
        self.reset()
        Parser.__init__(self, *args, **kwargs)

    def chart(self, *args, **kwargs):
        self.reset()
        return Parser.chart(self, *args, **kwargs)

    predict = capped(Parser.predict)
    scan = capped(Parser.scan)
    complete = capped(Parser.complete)


class FactsParser:
    def __init__(self):
        QUOTE = in_(QUOTES)
        HYPHEN = dictionary(['-', '—', '–'])
        self.parser_name = NamesExtractor(MorphVocab())

        Department = fact(
            'Department',
            ['definition', 'name', 'position']
        )

        POSITION = rule(
            morph_pipeline([
                'доцент',
                'аспирант',
                'ассистент',
                'профессор'
            ])
        )

        NAME = rule(
            QUOTE,
            not_(QUOTE).repeatable(),
            QUOTE
        )
        DEFINITION = rule(
            morph_pipeline(['кафедра', 'отдел']),
            NAME
        ).interpretation(Department.definition)
        POSITION_SET = rule(HYPHEN, POSITION.interpretation(Department.position))

        department = rule(DEFINITION, POSITION_SET).interpretation(Department)

        self.parser_department = CappedParser(department)

        DISERTATION_TYPE = rule(
            morph_pipeline([
                "кандидатская",
                "докторская",
                "магистерская"
            ])
        )

        Thesis = fact(
            'Thesis',
            ['kind', 'title', 'speciality', 'degree', 'branch']
        )

        TITLE = rule(
            not_(QUOTE).repeatable().optional(),
            QUOTE,
            not_(QUOTE).repeatable().interpretation(Thesis.title),
            QUOTE
        )

        THESIS_NAME = rule(
            DISERTATION_TYPE.optional().interpretation(Thesis.kind),
            morph_pipeline(['диссертация']),
            TITLE
        ).interpretation(Thesis)

        DEGREE_TYPE = rule(
            or_(normalized('кандидат'), normalized('доктор'))
        )

        Speciality = fact(
            'Speciality',
            ['code', 'hyphen', 'name']
        )

        SPECIALITY_CODE = rule(
            rule(
                INT.repeatable(),
                eq('.'),
                INT.repeatable(),
                eq('.'),
                INT.repeatable()
            ).interpretation(Speciality.code),
            HYPHEN.interpretation(Speciality.hyphen)
        )

        SPECIALITY_TITLE = rule(
            SPECIALITY_CODE,
            or_(rule(
                QUOTE,
                not_(QUOTE).repeatable().interpretation(Speciality.name),
                QUOTE
            ), rule(
                not_(or_(
                    eq('.'),
                    eq(';'))
                ).repeatable().interpretation(Speciality.name)
            ))
        ).interpretation(Speciality)

        SCIENCE_DIRECTION = rule(
            morph_pipeline([
                'направление',
                'специальность'
            ])
        )

        Branch = fact(
            'Branch',
            ['name']
        )

        BRANCH = rule(
            not_(eq('наук')).repeatable().interpretation(Branch.name.normalized()),
        ).interpretation(Branch)

        AcademicDegree = fact(
            'AcademicDegree',
            ['degree', 'branch', 'suffix']
        )

        ACADEMIC_DEGREE = rule(
            DEGREE_TYPE.interpretation(AcademicDegree.degree.normalized()),
            BRANCH.interpretation(AcademicDegree.branch),
            eq('наук').interpretation(AcademicDegree.suffix)
        ).interpretation(AcademicDegree)

        SPECIALITY_DEGREE = rule(
            not_(or_(eq('кандидата'), eq('доктора'))).repeatable(),
            ACADEMIC_DEGREE.interpretation(Thesis.degree)
        )

        SPECIALITY = rule(
            SPECIALITY_DEGREE.optional(),
            eq('по'),
            SCIENCE_DIRECTION,
            SPECIALITY_TITLE.interpretation(Thesis.speciality)
        )

        thesis = rule(THESIS_NAME, SPECIALITY.optional()).interpretation(Thesis)

        self.parser_thesis = CappedParser(thesis)

    def get_facts(self, text):
        facts = OntoFacts()
        matches = self.parser_name(text)
        match = [_.fact for _ in matches][0]
        if match.first is not None:
            # remove None
            fio = [x for x in [match.last, match.first, match.middle] if x is not None]
            facts.add_fact('Scientist', ' '.join(fio))

        for match in self.parser_department.findall(text):
            facts.add_fact('Department', match.fact.definition)

        for match in self.parser_thesis.findall(text):
            info = [
                ['Thesis', match.fact.title],
            ]
            if match.fact.speciality:
                if match.fact.speciality.code:
                    if match.fact.speciality.hyphen:
                        info.append(['Speciality', " ".join([
                            match.fact.speciality.code,
                            match.fact.speciality.hyphen,
                            match.fact.speciality.name
                        ])])
                    else:
                        info.append(['Speciality', " ".join([
                            match.fact.speciality.code,
                            match.fact.speciality.name
                        ])])
                else:
                    info.append(['Speciality', match.fact.speciality.name])

            if match.fact.degree:
                info.append(['AcademicDegree', match.fact.degree.degree])
                info.append(['BranchOfScience', match.fact.degree.branch.name])

            facts.add_facts(info)

        return facts


def join_spans(text, spans):
    spans = sorted(spans)
    return ' '.join(
        text[start:stop]
        for start, stop in spans
    )


def get_xml(items, url):
    xml = ET.Element('fdo_objects')
    document = ET.SubElement(xml, 'document')
    document.set('url', url)
    document.set('date', '')
    facts_element = ET.SubElement(document, 'facts')
    for item in items:
        fact_element = ET.SubElement(facts_element, 'Fact')
        fact_element.set('FactID', str(item.id))
        fact_element.set('LeadID', str(item.id))
        for f in item.facts:
            if f.value:
                field = ET.SubElement(fact_element, f.type)
                field.set('val', f.value)

    return ET.tostring(xml, encoding='utf-8', method='xml').decode('utf-8')


def pretty_print(xml):
    if xml:
        print(parseString(xml).toprettyxml())
    else:
        print('No facts found')

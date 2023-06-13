# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

from natasha import NamesExtractor, MorphVocab, Segmenter, Doc, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser
from natasha.grammars.addr import DOT, INT
from yargy import Parser, rule, not_, or_, predicates
from yargy.interpretation.normalizer import Normalizer
from yargy.predicates import (
    eq, type, caseless, in_, in_caseless,
    gte, lte, length_eq,
    is_capitalized, normalized,
    dictionary, gram,
)
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy.predicates import eq
from yargy.relations import gnc_relation
from yargy.tokenizer import (
    QUOTES,
    LEFT_QUOTES,
    RIGHT_QUOTES,

    MorphTokenizer,
    TokenRule, OTHER, EOL
)

from app.ontology import OntoFacts, OntoGroup, OntoFact


def join_spans(text, spans):
    spans = sorted(spans)
    return ' '.join(
        text[start:stop]
        for start, stop in spans
    )


def get_facts(text):
    QUOTE = in_(QUOTES)
    HYPHEN = dictionary(['-', '—', '–'])
    facts = OntoFacts()

    parser = NamesExtractor(MorphVocab())
    matches = parser(text)
    match = [_.fact for _ in matches][0]
    if match.first is not None:
        # remove None
        fio = [x for x in [match.last, match.first, match.middle] if x is not None]
        facts.add_fact('Scientist', ' '.join(fio))

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

    parser = Parser(department)
    for match in parser.findall(text):
        facts.add_fact('Department', match.fact.definition)

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

    parser = Parser(thesis)
    for match in parser.findall(text):
        info = [
            ['Thesis ', match.fact.title],
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

    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    segmenter = Segmenter()
    doc = Doc(text)

    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)

    return facts


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
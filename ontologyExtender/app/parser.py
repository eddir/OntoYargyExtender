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


def main():
    resume = """Авдеева Инга Анатольевна

кандидат экономических наук
Социально-экономический институт — кафедра "Таможенного дела и товароведения" — Доцент
Научная тематика
Экономика образования
Экономика социальной сферы
Конкурентные отношения в непроизводственной сфере

Образование и карьера
1988 - окончила исторический факультет Саратовского государственного института имени Н.Г. Чернышевского.

1995 – 1996 - обучалась в очной аспирантуре Саратовского государственного педагогического института имени К.А. Федина по специальности «политическая экономия».

2005 - присвоена ученая степень кандидата экономических наук. Защищена кандидатская диссертация на тему «Теоретико-методологические аспекты управления социальной сферой в условиях формирования конкурентных отношений».

Награды:
Почетная грамота Министерства образования Саратовской области (2011 г.)
Повышение квалификации
2015 - В Поволжском институте управления имени П.А.Столыпина (филиале) РАНХ и ГС по программе "Инновационные технологии в образовательном процессе" с 20 мая по 26 июня 2015 г. в объеме 36 часов (сертификат № 180)

2017 - В Саратовском социально-экономическом институте (филиале) ФГБОУ ВО "Российский экономический университет имени Г.В. Плеханова по дополнительной профессиональной программе "Современные психолого-педагогические технологии профессионального обучения" 12 октября 2017 г. в объеме 72 часов (удостоверение о повышении квалификации;

2017 - В Саратовском социально-экономическом институте (филиале) ФГБОУ ВО "Российский экономический университет имени Г.В. Плеханова по дополнительной профессиональной программе "Электронная информационно-образовательная среда вуза" 23 ноября 2017 г. в объеме 36 часов (удостоверение о повышении квалификации).

2017 - Повышении квалификации по дополнительной профессиональной программе «Теория и практика преподавания бюджетной грамотности» в объеме 36 часов. Обучение проходило в ФГБОУ ВО «Российский экономический университет имени Г.В. Плеханова» с 28 августа 2017 года по 08 сентября 2017 года, регистрационный номер 5245-УД, дата выдачи 08 сентября 2017 года, город Москва.

2019 - Профессиональная переподготовка по программе «Менеджмент в образовании» в объеме 504 часов. Обучение проходило в Саратовском социально-экономическом институте (филиале) ФГБОУ ВО «Российский экономический университет имени Г.В. Плеханова» с 02 сентября 2019 года по 02 декабря 2019 года, регистрационный номер 2598-ППК, дата выдачи 02 декабря 2019 года, город Саратов.

2020 - Повышении квалификации по дополнительной профессиональной программе «Функционирование электронной информационно-образовательной среды образовательной организации высшего образования» в объеме 72 часов. Обучение проходило в Саратовском социально-экономическом институте (филиале) ФГБОУ ВО «Российский экономический университет имени Г.В. Плеханова» с 23 декабря 2019 года по 23 января 2020, регистрационный номер 10100-УД, дата выдачи 23 января 2020 года, город Саратов.

Основные публикации
Автор учебных и научных работ. Всего 31 публикация, общим объемом 13  п. л/

Научные статьи:

Управление социальной сферой как системой в условиях рыночных отношений. Социальные и духовные основания общественного развития. Межвузовский научный сборник. - Саратов. Научная книга, 2004г (0,3 п.л.);
Методологические аспекты управления вузом в современных условиях. Наука и современное развитие Российского государства и общества: сб.науч.статей. - Саратов: Поволжский институт управления им. П.А.Столыпина, 2014. -124 с. ISBN 978-5-8180-0465-5 (5.63 п.л.(авторских 0,4 п.л.))
Фактор доверия в формировании институционального климата Российского общества//Вестник Саратовского государственного социально-экономического университета. 2017. № 5 (69). С.9-13 (0,5 п.л.)
Методы борьбы с теневой экономикой в странах ЕС // Вестник Саратовского государственного социально-экономического университета. 2018. № 2 (71) (0,5 п.л.)
Конкурентные отношения в социальной сфере //Научное обозрение "Актуальные проблемы и перспективы развития экономики: российский и зарубежный опыт". Выпуск № 16. М., 2018.С. 5-8.
Тенденции повышения уровня жизни населения в России //Вестник Саратовского государственного социально-экономического университета. 2019. № 1 (75). С.22-25 (0,5 п.л.)
Развитие экономического потенциала России: условия, барьеры, возможности. Коллективная монография/ По общ. ред. Н.Г.Барашова, Е.А.Ореховой. Саратов, 2018 г. С. 91-101
Экономическая эффективность: проблемы теории и практики в условиях выхода из экономического кризиса. / Под общей редакцией М.В. Попова. Саратов, 2020. С. 22-25
Учебные пособия: 

Региональная экономика и управление. (Учебное пособие) - Саратов: ИЦ «РАТА», 2009. – 318 с.,ISBN 978-5-91659-071-5 ( 20 п.л. (авторских 1 п.л.));
Практикум по экономическим дисциплинам / Под ред. Е.Ш. Курмакаевой и П.И. Прошунина. Гл.3, 5-9. - Саратов: Издательство "Буква", 2015.-100 с.
Экономическая теория: Микроэкономика (Учебное пособие для студентов, обучающихся по направлению подготовки 38.03.01 "Экономика") - Саратов: Саратовский социально-экономический институт (филиал) РЭУ им Г.В. Плеханова, 2016.- 196 с. ISBN 978-5-4345-0406-5 (10,8 п.л. (авторских 0,7 п.л.))
История экономических учений /учебно-методическое пособие для студентов направления подготовки 38.03.01 Экономика, специальности 38.05.01 Экономическая безопасность. Саратов, 2018. С. 58-64

"""
    facts = get_facts(resume)
    pretty_print(get_xml(facts, "\\shulga_tatyana_erikovna.xml"))


if __name__ == '__main__':
    main()

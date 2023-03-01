from pprint import pprint


class OntoFact:
    def __init__(self, fact_type, value):
        self.type = fact_type
        self.value = value

    def __str__(self):
        return f'{self.type}: {self.value}'


class OntoGroup:
    def __init__(self, group_id: int):
        self.id = group_id
        self.facts = []

    def __str__(self):
        return f'Group {self.id}: {[str(f) for f in self.facts]}'

    def __iter__(self):
        return iter(self.facts)

    def add_fact(self, f):
        self.facts.append(f)

    def add_facts(self, facts: list):
        for f in facts:
            self.facts.append(f)

    def get_all(self):
        return self.facts


class OntoFacts:
    def __init__(self):
        self.groups = []
        self.last_id = 0

    def __iter__(self):
        return iter(self.groups)

    def __str__(self):
        return f'OntoFacts: {[str(g) for g in self.groups]}'

    def as_array(self):
        array = []
        for group_ in self.groups:
            for fact_ in group_:
                array.append([fact_.type, fact_.value])
        return array

    def add_group(self, group: OntoGroup):
        group.id = self.last_id
        self.last_id += 1
        self.groups.append(group)

    def add_fact(self, fact_type, value):
        group = OntoGroup(self.last_id)
        group.add_fact(OntoFact(fact_type=fact_type, value=value))
        self.add_group(group)

    def add_facts(self, facts: list):
        group = OntoGroup(self.last_id)
        for f in facts:
            group.add_fact(OntoFact(fact_type=f[0], value=f[1]))
        self.add_group(group)


if __name__ == "__main__":
    facts = OntoFacts()
    facts.add_fact('name', 'Иванов Иван Иванович')
    facts.add_fact('url', 'https://www.sstu.ru/teachers/ivanov-ivan-ivanovich/')
    group = OntoGroup(0)
    group.add_facts([
        OntoFact('name', 'Иванов Иван Иванович'),
        OntoFact('url', 'https://www.sstu.ru/teachers/ivanov-ivan-ivanovich/'),
        OntoFact('type', 'Преподаватель'),
    ])
    facts.add_group(group)
    fact = [f for g in facts for f in g if f.type == 'name'][0]
    print(fact.value)
    pprint(facts.__str__())

from src.Person import Person


class FamilyTree:
    def __init__(self, factory):
        print("Reading files...")
        self.factory = factory

        print("Generating family tree...")
        self.roots = []
        self._create_family_tree()

    def _create_family_tree(self):
        year_born = 1950
        decade = '1950s'
        life_exp_1 = self.factory.generate_life_exp(year_born)
        year_died_1 = year_born + life_exp_1
        first_name_1 = 'Molly'
        last_name = 'Jones'
        gender_1 = 'female'
        person_1 = Person(year_born=year_born,
                          year_died=year_died_1,
                          first_name=first_name_1,
                          last_name=last_name,
                          gender=gender_1)

        life_exp_2 = self.factory.generate_life_exp(year_born)
        year_died_2 = year_born + life_exp_2
        first_name_2 = 'Desmond'
        gender_2 = 'male'

        person_2 = Person(year_born=year_born,
                          year_died=year_died_2,
                          first_name=first_name_2,
                          last_name=last_name,
                          gender=gender_2)

        person_1.partner = person_2
        person_2.partner = person_1

        self.roots = [person_1, person_2]

        children = self.factory.create_children(person=person_1, decade=decade)
        person_1.children = person_2.children = children

    def _collect_all_people(self):
        visited = set()
        people = []

        def search(person):
            if person in visited:
                return

            visited.add(person)
            people.append(person)

            for child in person.children:
                search(child)

            if person.has_partner():
                search(person.partner)

        for root in self.roots:
            search(root)

        return people

    def total_people(self):
        return len(self._collect_all_people())

    def total_people_by_decade(self):
        people = self._collect_all_people()

        people_by_decade = {}
        for decade in range(1950, 2120, 10):
            people_by_decade[decade] = sum(x.is_alive_in_decade(decade) for x in people)

        return people_by_decade

    def duplicate_names(self):
        people = self._collect_all_people()

        result = set()
        visited = set()
        for person in people:
            if person.get_full_name() in visited:
                result.add(person.get_full_name())
            else:
                visited.add(person.get_full_name())

        return result

    def _pretty_print(self, person, indent="", is_last=True, visited=None):
        if visited is None:
            visited = set()

        if person in visited:
            print(f"{indent}└── [Already Listed: {person.get_full_name()}]")
            return
        visited.add(person)

        marker = "└── " if is_last else "├── "

        partner_info = f" <> (Partner: {person.partner.first_name})" if person.has_partner() else ""
        print(f"{indent}{marker}{person} [{person.gender}]{partner_info}")

        if person.has_children():
            new_indent = indent + ("    " if is_last else "│   ")
            for i, child in enumerate(person.children):
                last_child = (i == len(person.children) - 1)
                self._pretty_print(child, new_indent, last_child, visited)

    def pretty_print(self):
        self._pretty_print(self.roots[0])

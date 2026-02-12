class Person:
    def __init__(self, year_born, year_died, first_name, last_name, gender):
        self.year_born = year_born
        self.year_died = year_died
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender

        self.partner = None
        self.children = []

    def get_year_born(self):
        return self.year_born

    def get_year_died(self):
        return self.year_died

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_gender(self):
        return self.gender

    def get_partner(self):
        return self.partner

    def get_children(self):
        return self.children

    def set_partner(self, partner):
        self.partner = partner

    def set_children(self, children):
        self.children = children

    def is_alive_in_year(self, year):
        return self.year_born <= year <= self.year_died

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return (
            f"{self.get_full_name()} "
            f"({self.year_born}-{self.year_died})"
        )
class Person:
    """Represents an individual in the family tree."""

    def __init__(self, year_born, year_died, first_name, last_name, gender):
        self.year_born = year_born
        self.year_died = year_died
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender

        self.decade = str((self.year_born // 10) * 10) + "s"
        self.partner = None
        self.children = []

    def has_partner(self):
        return self.partner is not None

    def has_children(self):
        return len(self.children) > 0

    def is_alive_in_decade(self, decade):
        return (self.year_born <= decade + 9) and (decade <= self.year_died)

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return (
            f"{self.get_full_name()} "
            f"({self.year_born}-{self.year_died})"
        )

import random
import csv
import math

from src.Person import Person


class PersonFactory:
    """Factory responsible for generating the people and their relationships."""

    def __init__(self, folder):
        # Data containers for demographic statistics
        self.life_expectancy_data = {}
        self.first_names_data = {}
        self.last_names_data = {}
        self.gender_probability_data = {}
        self.birth_marriage_data = {}
        self.rank_to_probability = []

        # Load all required CSV data
        self.read_files(folder)

    def read_files(self, folder):
        """Read CSV files into memory."""

        # Load first name data by decade and gender
        with open(folder + 'first_names.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                decade = row["decade"]
                gender = row["gender"]
                name = row["name"]
                frequency = float(row["frequency"])

                if decade not in self.first_names_data:
                    self.first_names_data[decade] = {}

                if gender not in self.first_names_data[decade]:
                    self.first_names_data[decade][gender] = []

                self.first_names_data[decade][gender].append((name, frequency))

        # Load last name rankings by decade
        with open(folder + 'last_names.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                decade = row["Decade"]
                rank = int(row["Rank"])
                last_name = row["LastName"]

                if decade not in self.last_names_data:
                    self.last_names_data[decade] = []

                self.last_names_data[decade].append((last_name, rank))

        # Load life expectancy data by birth year
        with open(folder + 'life_expectancy.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                year = int(row["Year"])
                life_exp_at_birth = float(row["Period life expectancy at birth"])
                self.life_expectancy_data[year] = life_exp_at_birth

        # Load gender probability data by decade
        with open(folder + 'gender_name_probability.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                decade = row["decade"]
                gender = row["gender"]
                probability = float(row["probability"])

                if decade not in self.gender_probability_data:
                    self.gender_probability_data[decade] = {}

                self.gender_probability_data[decade][gender] = probability

        # Load birth and marriage rates by decade
        with open(folder + 'birth_and_marriage_rates.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                decade = row["decade"]
                birth_rate = float(row["birth_rate"])
                marriage_rate = float(row["marriage_rate"])

                self.birth_marriage_data[decade] = {"birth_rate": birth_rate, "marriage_rate": marriage_rate}

        # Load rank-to-probability mapping for last names
        with open(folder + 'rank_to_probability.csv') as file:
            line = file.readline().strip()
            probabilities = line.split(',')

            self.rank_to_probability = [float(p) for p in probabilities]

    def create_person(self, year_born, last_name=None, is_partner=False):
        """Create a person and recursively generate descendants."""

        decade = str((year_born // 10) * 10) + "s"

        first_name, gender = self.choose_gender_first_name(decade)

        if last_name is None:
            last_name = self.choose_last_name(decade)

        life_exp = self.generate_life_exp(year_born)
        year_died = int(year_born + life_exp)

        person = Person(
            year_born=year_born,
            year_died=year_died,
            first_name=first_name,
            last_name=last_name,
            gender=gender
        )

        if is_partner:
            return person

        # Determine if the person marries
        probability = self.birth_marriage_data[decade]["marriage_rate"]
        if random.random() < probability:
            partner = self.create_partner(person=person)
            person.partner = partner

        if person.has_partner():
            if person.year_born < person.partner.year_born:
                elder_partner = person
                elder_decade = person.decade
            else:
                elder_partner = person.partner
                elder_decade = person.partner.decade

            person.children = self.create_children(elder_partner, elder_decade)
            person.partner.children = person.children
        else:
            person.children = self.create_children(person, person.decade)

        return person

    # Generate children
    def create_partner(self, person):
        """Create a partner within a +- 10-year age range."""

        year_born = person.year_born + random.randint(-10, 10)
        if year_born > 2120:
            return None

        partner = self.create_person(year_born=year_born, is_partner=True)

        return partner

    def create_children(self, person, decade):
        """Generate children based on birth rate statistics."""

        rate = self.birth_marriage_data[decade]["birth_rate"]

        # Determine possible number of children (+- 1.5 children range)
        min_children = max(math.ceil(rate - 1.5), 0)
        max_children = math.ceil(rate + 1.5)

        # Reduce children by 1 if no partner
        if not person.has_partner():
            min_children = max(min_children - 1, 0)
            max_children = max(max_children - 1, 0)

        num_children = random.randint(min_children, max_children)

        start_year = person.year_born + 25
        end_year = person.year_born + 45

        children = []

        if num_children > 0:
            spacing = (end_year - start_year) / (num_children + 1)

            for i in range(num_children):
                child_year = int(start_year + spacing * (i + 1))

                if child_year > 2120:
                    continue

                if person.has_partner():
                    child_last_name = random.choice([person.last_name, person.partner.last_name])
                else:
                    child_last_name = person.last_name

                child = self.create_person(year_born=child_year, last_name=child_last_name)
                children.append(child)

        return children

    def generate_life_exp(self, year_born):
        """Generate life expectancy with random variation."""

        base = self.life_expectancy_data[year_born]
        variation = random.randint(-10, 10)
        return int(base + variation)

    def choose_gender_first_name(self, decade):
        """Select gender and first name."""

        gender_data = self.gender_probability_data[decade]

        genders = list(gender_data.keys())
        probabilities = list(gender_data.values())

        chosen_gender = random.choices(genders, weights=probabilities, k=1)[0]

        names_data = self.first_names_data[decade][chosen_gender]

        names = []
        frequencies = []

        for name, frequency in names_data:
            names.append(name)
            frequencies.append(frequency)

        chosen_name = random.choices(names, weights=frequencies, k=1)[0]

        return chosen_name, chosen_gender

    def choose_last_name(self, decade):
        """Select last name based on rank-weighted probability."""

        names_with_ranks = self.last_names_data[decade]

        names = []
        weights = []

        for name, rank in names_with_ranks:
            probability = self.rank_to_probability[rank - 1]
            names.append(name)
            weights.append(probability)

        return random.choices(names, weights=weights, k=1)[0]

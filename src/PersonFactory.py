import random
import csv

from src.Person import Person


class PersonFactory:
    def __init__(self, folder):
        self.life_expectancy_data = {}
        self.first_names_data = {}
        self.last_names_data = {}
        self.gender_probability_data = {}
        self.birth_marriage_data = {}
        self.rank_to_probability = []

        ## Init data
        self.read_files(folder)

    def read_files(self, folder):
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

        with open(folder + 'last_names.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                decade = row["Decade"]
                rank = int(row["Rank"])
                last_name = row["LastName"]

                if decade not in self.last_names_data:
                    self.last_names_data[decade] = []

                self.last_names_data[decade].append((last_name, rank))

        with open(folder + 'life_expectancy.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                year = int(row["Year"])
                life_exp_at_birth = float(row["Period life expectancy at birth"])
                self.life_expectancy_data[year] = life_exp_at_birth

        with open(folder + 'gender_name_probability.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                decade = row["decade"]
                gender = row["gender"]
                probability = float(row["probability"])

                if decade not in self.gender_probability_data:
                    self.gender_probability_data[decade] = {}

                self.gender_probability_data[decade][gender] = probability

        with open(folder + 'birth_and_marriage_rates.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                decade = row["decade"]
                birth_rate = float(row["birth_rate"])
                marriage_rate = float(row["marriage_rate"])

                self.birth_marriage_data[decade] = {"birth_rate": birth_rate, "marriage_rate": marriage_rate}

        with open(folder + 'rank_to_probability.csv') as file:
            line = file.readline().strip()
            probabilities = line.split(',')

            self.rank_to_probability = [float(p) for p in probabilities]


    def create_person(self, year_born, last_name=None, is_partner=False):
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

        probability = self.birth_marriage_data[decade]["marriage_rate"]
        if random.random() < probability:
            partner = self.create_partner(person=person)
            person.partner = partner



        return person


    def create_partner(self, person):
        year_born = person.year_born + random.randint(-10, 10)
        partner = self.create_person(year_born=year_born, is_partner=True)

        return partner

    def determine_children_count(self, person, decade):
        probability = self.birth_marriage_data[decade]["birth_rate"]

        has_children = random.random() < probability
        # TODO


    def generate_life_exp(self, year_born):
        base = self.life_expectancy_data[year_born]
        variation = random.randint(-10, 10)
        return base + variation

    def choose_gender_first_name(self, decade):
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

        chosen_name = random.choices(names, weights = frequencies, k = 1)[0]

        return chosen_name, chosen_gender

    def choose_last_name(self, decade):
        names_with_ranks = self.last_names_data[decade]

        names = []
        weights = []

        for name, rank in names_with_ranks:
            probability = self.rank_to_probability[rank - 1]
            names.append(name)
            weights.append(probability)

        return random.choices(names, weights = weights, k = 1)[0]
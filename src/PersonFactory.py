import random
import csv


class PersonFactory:
    def __init__(self):
        self.life_expectancy_data = {}
        self.first_names_data = {}
        self.last_names_data = {}
        self.gender_probability_data = {}

    def read_files(self):
        with open('first_names.csv', newline="") as csvfile:
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

        with open('last_names.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                decade = row["Decade"]
                rank = int(row["Rank"])
                last_name = row["LastName"]

                if decade not in self.last_names_data:
                    self.last_names_data[decade] = []

                self.last_names_data[decade].append((last_name, rank))

        with open('life_expectancy.csv', newline="") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                year = row["Year"]
                life_exp_at_birth = float(row["Period life expectancy at birth"])

                if year not in self.life_expectancy_data:
                    self.life_expectancy_data[year] = {}

                self.life_expectancy_data[year].append(life_exp_at_birth)

    def create_person(self, year_born, last_name=None):
        pass

    def create_partner(self, person):
        pass

    def determine_children_count(self, person):
        pass
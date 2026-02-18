from src.FamilyTree import FamilyTree
from src.PersonFactory import PersonFactory



def menu(tree):
    response = input("""Are you interested in:
(T)otal number of people in the tree
Total number of people in the tree by (D)ecade
(N)ames duplicated
(P)retty print
""").upper()

    if response == "T":
        print("The tree contains " + str(tree.total_people()) + " people total")
    elif response == "N":
        duplicates = tree.duplicate_names()
        print("There are " + str(len(duplicates)) + " duplicate names in the tree")
        for name in duplicates:
            print(" * " + name)
    elif response == "D":
        by_decade = tree.total_people_by_decade()
        for decade in by_decade:
            print(" * " + str(decade) + ": " + str(by_decade[decade]))
    elif response == "P":
        tree.pretty_print()
    else:
        print("Invalid input: " + response)

    menu(tree)

if __name__ == '__main__':
    factory = PersonFactory("C:\\Users\\jlwis\\PycharmProjects\\assignment-01-kids-in-the-yard-jlwise0111\\data\\")
    tree = FamilyTree(factory)
    menu(tree)
"""Generating association rules with confidence at least c
from the itemsets found in the first step."""

import time
from DataLoader import DataLoader
from Support import Support
from itertools import combinations
from tabulate import tabulate



class Confidence:

    def __init__(self):
        pass

    @staticmethod
    def _get_all_subsets(itemset):
        """
        A generator returning all possible subsets as frozensets
        :param itemset: set of items
        :return: subsets
        """
        for i in range(1, len(itemset)):
            for subset in combinations(itemset, i):
                yield frozenset(subset)


    @staticmethod
    def get_association(itemsets, c):
        """

        :param itemsets: Dict with (key, value) = (frozenset({items}), support), support > s
        :param c: minimum conficence (float on [0,1])
        :return: associations, list of tuples (X, Y) where each tuple is a rule X -> Y
        """
        associations = []

        # calculating association rules as the rules X -> Y where
        # conf(X->Y) = support(X U Y) / support(X) is minimum c
        for X_and_Y, X_and_Y_count in itemsets.items():
            for X in Confidence._get_all_subsets(X_and_Y):
                c_X_Y = 1.0 * X_and_Y_count / itemsets[X]
                if c_X_Y >= c:
                    associations.append((X, (X_and_Y - X)))

        return associations

    @staticmethod
    def print_associations(associations):
        rules = [[set(a[0]), '=>', set(a[1])] for a in associations]
        print(tabulate(rules, headers=["From", "", "to"]))


if __name__ == '__main__':
    """
    This method is an example usage of the class responsible for getting the associations.
    """
    file_path = 'Data/T10I4D100K.dat'
    c = 0.5  # Min confidence
    s = 1000  # Min support

    start = time.time()  # Time tracking
    data_loader = DataLoader(file_path)  # Load the data
    basket_occurrences = data_loader.get_item_occurrences()

    # Get itemsets with at least support s
    support = Support()
    itemsets = support.count_support(basket_occurrences, s=s)

    # Get and print found associations
    associations = Confidence.get_association(itemsets, c=c)
    print("---------------------------")
    print("Found associations:")
    Confidence.print_associations(associations)
    print("Run time: " + str(time.time() - start))  # Print time

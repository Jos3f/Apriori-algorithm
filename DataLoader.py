"""
Loads and reads a dataset of sales transactions,
where each row is a basket of hash values.
"""

class DataLoader:
    def __init__(self, file_path):
        self.baskets = [set([int(item) for item in line.split()]) for line in open(file_path).readlines()]
        self.occurrences = None
        self.nr_baskets = len(self.baskets)

    def get_baskets(self):
        """
        :return: List of all baskets represented as sets of unique items
        """
        return self.baskets

    def get_item_occurrences(self, nr_baskets=None):
        """
        Iterates over the baskets and registers which baskets contain each item
        :return: Dict with (key, value) = (item, set of baskets containing that item)
        """
        if nr_baskets == None:
            nr_baskets = len(self.baskets)
        if self.occurrences is None or self.nr_baskets != nr_baskets:
            self.occurrences = {}
            self.nr_baskets = nr_baskets
            for basket_idx, basket in enumerate(self.baskets[:nr_baskets]):
                for item in basket:
                    if item in self.occurrences:
                        self.occurrences[item].add(basket_idx)
                    else:
                        self.occurrences[item] = {basket_idx}

        return self.occurrences


if __name__ == "__main__":
    # Example of how to use this class
    file_path = 'Data/T10I4D100K.dat'
    data_loader = DataLoader(file_path)
    baskets = data_loader.get_baskets()
    print(baskets[0])




import time
from tqdm import tqdm
from itertools import combinations

from DataLoader import DataLoader


class Support:
    """Finding frequent itemsets with support at least s"""
    def __init__(self):
        pass

    def count_support(self, occurrences, s=500):
        """
        Using A-Priori Algorithm to find itemsets with support of at least s
        :param occurrences: Dict with (key, value) = (item, set of baskets containing that item)
        :param s: support (int)
        :return: itemsets (Dict with (key, value) = (frozenset({items}), support))
        """
        itemsets = {}

        # 1st pass to count frequency of singletons
        L_1 = set()
        for item, positions in occurrences.items():
            if len(positions) >= s:
                L_1.add(frozenset({item}))
                itemsets[frozenset({item})] = len(positions)

        # pass nr k
        L_k = L_1.copy()
        # C_k = set([x.union(y) for x, y in itertools.product(L_k, L_1) if not y.issubset(x)])

        enter = True
        pass_nr = 0
        while enter:
            enter = False
            prev_itemsets = {}
            C_k, max_length = self._get_product_generator(L_k, L_1, itemsets)
            # for itemset in tqdm(set([x.union(y) for x, y in itertools.product(L_k, L_1) if not y.issubset(x)])): # Faster but requires more memory

            for itemset in tqdm(C_k, total=max_length):
                # stopping criterion when no new candidates can be found
                if itemset in prev_itemsets:
                    continue
                enter = True
                intersecting_baskets = None
                for item in itemset:
                    if intersecting_baskets is None:
                        intersecting_baskets = occurrences[item].copy()
                    else:
                        # Remove the items that is not present in both intersecting_baskets and occurrences[item]
                        intersecting_baskets.intersection_update(occurrences[item])
                prev_itemsets[itemset] = len(intersecting_baskets)

            L_k = set()
            # Store only candidate k-tuples with at least support s and update itemsets to be previous itemset
            for itemset in prev_itemsets:
                if prev_itemsets[itemset] >= s:
                    L_k.add(itemset)
                    itemsets[itemset] = prev_itemsets[itemset]

            pass_nr += 1
            # C_k = set([x.union(y) for x, y in itertools.product(L_k, L_1) if not y.issubset(x)])

        return itemsets

    def _get_product_generator(self, L_k, L_1, itemsets):
        """

        :param L_k: set of elements frozenset({item})
        :param L_1: set of elements frozenset({item})
        :param itemsets: Dict with (key, value) = (frozenset({item}), support)
        :return: product_generator, largest total number of candidates
        """

        largest_total = len(L_k) * len(L_1)

        def product_generator(L_k, L_1):
            """
            Does the same as: C_k = set([x.union(y) for x, y in itertools.product(L_k, L_1) if not y.issubset(x)])
            but as a generator for memory efficiency
            :param L_k: set of elements frozenset({item})
            :param L_1: set of elements frozenset({item})
            :return: yields new itemsets, where every subset, of size K-1, in the new item set exists in previous itemsets
            """

            # Generator approach may cause duplicates, but it is more memory efficient
            for y in L_1:
                for x in L_k:
                    if not y.issubset(x):
                        new_itemset = x.union(y)
                        # Pruning step, check that every subset, of size K-1, in the new item set exists in itemsets.
                        possible_subsets = combinations(new_itemset, len(new_itemset) - 1)
                        subsets_larger_than_s = [frozenset(itemset) in itemsets for itemset in possible_subsets]
                        if all(subsets_larger_than_s):
                            yield new_itemset

        return product_generator(L_k, L_1), largest_total


if __name__ == '__main__':
    """
    Example usage of class that takes a dataset of items in baskets and returns the itemsets with at least a given 
    support s together with their counts. 
    """
    

    file_path = 'Data/T10I4D100K.dat'  # Data set path
    s = 1000  # Support

    start = time.time()  # Time tracking

    # Load data
    data_loader = DataLoader(file_path)
    basket_occurrences = data_loader.get_item_occurrences()

    # Get and print itemsets with at least support s
    support = Support()
    result = support.count_support(basket_occurrences, s=s)
    print("Distinct item sets found: {}".format(len(result)))
    for i in result:
        print(i, ":", result[i])


    print("Time: ", time.time() - start) # Time tracking
    pass

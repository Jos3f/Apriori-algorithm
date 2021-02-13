from pathlib import Path
import argparse
from tabulate import tabulate

from DataLoader import DataLoader
from Support import Support


def main(args):
    """
    Find frequent item sets and association rules, and print them.
    :param args: arguments
    :return:
    """

    task = tasks[args.task.lower()]

    # Load data
    data_loader = DataLoader(args.filename)
    basket_occurrences = data_loader.get_item_occurrences()

    if task == 0:
        # Get and print itemsets with at least support s
        print("Finding item sets with support {}:".format(args.support))
        support = Support()
        result = support.count_support(basket_occurrences, s=args.support)
        print("\nDistinct item sets found: {}".format(len(result)))
        data = [[set(i), result[i]] for i in result]
        print(tabulate(data, headers=["Item set", "Support"]))

    elif task == 1:
        pass

    return


# Default dataset path
filename = Path('Data/T10I4D100K.dat')
# Valid tasks
tasks = {'frequent': 0, 'association': 1}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tool for identifying frequent item sets and association rules in baskets, using the Apriori '
                    'algorithm.')
    parser.add_argument('-t', '--task', type=str, default='frequent', choices=tasks.keys(),
                        help='Task to perform.')
    parser.add_argument('-f', '--filename', type=str, default=filename,
                        help='Dataset path. The data should contain rows of space separated item indices where each '
                             'row corresponds to a basket.')
    parser.add_argument('-s', '--support', type=int, default=1000, help='The least support required to be '
                                                                          'considered frequent.')
    parser.add_argument('-c', '--confidence', type=float, default=0.5, help='The least confidence required for '
                                                                            'association rules.')

    args = parser.parse_args()

    main(args)

from pathlib import Path
import argparse
from tabulate import tabulate

from DataLoader import DataLoader
from Support import Support
from Confidence import Confidence
from Data.DataGen import generate_sample_data


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

    # Get item sets with at least support s
    print("Finding item sets with support {}:".format(args.support))
    support = Support()
    itemsets = support.count_support(basket_occurrences, s=args.support)
    print("\nDistinct item sets found: {}".format(len(itemsets)))

    if task == 0:
        # print found item sets
        data = [[set(i), itemsets[i]] for i in itemsets]
        print(tabulate(data, headers=["Item set", "Support"]))
    elif task == 1:
        # Get association rules
        print("Finding association rules with confidence of at least {}:".format(args.confidence))
        associations = Confidence.get_association(itemsets, c=args.confidence)
        print("Found associations:")
        Confidence.print_associations(associations)

    return


# Default dataset path
filename = Path('Data/example_dataset.dat')
# Valid tasks
tasks = {'frequent': 0, 'association': 1}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tool for identifying frequent item sets and association rules in baskets, using the Apriori '
                    'algorithm.')
    parser.add_argument('-t', '--task', type=str, default='frequent', choices=tasks.keys(),
                        help='Task to perform.')
    parser.add_argument('-f', '--filename', type=str, default=filename,
                        help='Dataset path. The data should contain rows of space-separated item indices where each '
                             'row corresponds to a basket.')
    parser.add_argument('-s', '--support', type=int, default=500, help='The least support required to be '
                                                                          'considered frequent.')
    parser.add_argument('-c', '--confidence', type=float, default=0.5, help='The least confidence required for '
                                                                            'association rules.')

    args = parser.parse_args()

    main(args)

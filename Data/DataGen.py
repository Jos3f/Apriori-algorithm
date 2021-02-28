import numpy as np
from tqdm import tqdm


def generate_sample_data(filename, item_count=1000, basket_count=100000, seed=123):
    print("Creating data set of {} baskets with {} unique items".format(basket_count, item_count))

    np.random.seed(seed)

    # Create item indices and probability of being selected in the first pass
    items = np.arange(item_count)
    item_selection_prob = np.random.exponential(1, item_count).clip(0, 2)
    item_selection_prob /= np.sum(item_selection_prob)

    # Create some associations
    item_assoc_prob = np.random.exponential(0.15, item_count).clip(0, 1)
    associated_to = {}

    for i, item in enumerate(items):
        sample_count = np.random.choice([1, 2, 3], 1, p=[.7, .2, .1])
        associated_to[item] = frozenset(np.random.choice(items, sample_count, replace=False))


    file1 = open(filename, "w")
    for _ in tqdm(range(basket_count)):
        item_count = np.random.lognormal(1.75, 0.4, 1).astype(int).clip(1)

        basket = set(np.random.choice(items, item_count, replace=False, p=item_selection_prob))
        basket_associated = set()
        for item in basket:
            if np.random.uniform(0,1) < item_assoc_prob[item]:
                basket_associated.update(associated_to[item])

        basket.update(basket_associated)
        file1.write(" ".join(str(item) for item in basket)+"\n" )

    file1.close()

    pass


if __name__ == '__main__':
    generate_sample_data("example_dataset.dat", 1000, 100000)
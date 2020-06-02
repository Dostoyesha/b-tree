import random

import btree

if __name__ == "__main__":

    rand_list = [random.randrange(1, 10) for _ in range(150)]
    # rand_list = [i for i in range(10)]
    # rand_list.reverse()

    tree = btree.BTree(3)

    for key in rand_list:
        tree.insert(key)

    tree.display()
    print(f"Узел и позиция (от нуля): {tree.search(2)}")

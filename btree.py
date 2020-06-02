from pprint import pprint


class Node(object):
    """A b-tree node.

    Attributes:
        is_leaf : boolean, determines whether this node is a leaf.
        keys : list of keys internal to this node.
        child_nodes : list of children of this node.
    """

    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.child_nodes = []

    def __str__(self):
        return f"{self.keys} -> {len(self.child_nodes)} childs"

    def __repr__(self):
        return f"{self.keys} -> {len(self.child_nodes)} childs"


class BTree(object):
    def __init__(self, min_degree=2):
        self.min_degree = min_degree
        self.root = Node(is_leaf=True)

    def split_child(self, parent, i):
        min_degree = self.min_degree

        child = parent.child_nodes[i]
        new_child = Node(is_leaf=child.is_leaf)

        parent.child_nodes.insert(i + 1, new_child)  # добавляем справа новый дочерний узел
        parent.keys.insert(i, child.keys[min_degree - 1])  # средний ключ переносим на новый верхний узел

        new_child.keys = child.keys[min_degree:]
        child.keys = child.keys[0:(min_degree - 1)]

        if not child.is_leaf:
            new_child.child_nodes = child.child_nodes[min_degree:]
            child.child_nodes = child.child_nodes[0:min_degree]

    def insert_non_full(self, node, key):
        """Вставляет ключ key в узел x, который при вызове этой функции не заполнен.

        При необходимости спускается рекурсивно вних по дереву, причем каждый узел, в который
        она входит - не заполнен, что обеспечивается вызовом insert(self, key).
        """
        i = len(node.keys) - 1

        if node.is_leaf:
            # вставить ключ в лист
            node.keys.append(0)
            while i >= 0 and key < node.keys[i]:  # идем с конца и сдвигаем вправо
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            # вставить key в подходящий лист в поддереве node
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            if len(node.child_nodes[i].keys) == (2 * self.min_degree) - 1:
                # если дочерний узел заполнен, разделяем его на два незаполненных
                self.split_child(node, i)
                if key > node.keys[i]:
                    # определяем, в какой узел должна спуститься рекурсия
                    i += 1
            self.insert_non_full(node.child_nodes[i], key)  # вставка ключа в соответствующее поддерево

    def insert(self, key):
        """Вставка ключа в дерево."""
        root = self.root
        if len(root.keys) == (2 * self.min_degree) - 1:
            # Если корень заполнен, то он разбивается и новый узел становится новым корнем
            new_node = Node()
            self.root = new_node
            new_node.child_nodes.insert(0, root)  # former root is now 0th child of new root s
            self.split_child(new_node, 0)
            self.insert_non_full(new_node, key)
        else:
            self.insert_non_full(root, key)

    def search(self, key, node=None):
        if node:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and key == node.keys[i]:
                return node, i
            elif node.is_leaf:
                return None
            else:
                return self.search(key, node.child_nodes[i])
        else:
            return self.search(key, self.root)

    def get_child_nodes(self, node):
        result = dict()

        if node.child_nodes:
            for child in node.child_nodes:
                child_key = tuple(child.keys)
                result[child_key] = self.get_child_nodes(child)

        return result

    def display(self):
        tree_display_dict = dict()
        root_key = tuple(self.root.keys)

        tree_display_dict[root_key] = self.get_child_nodes(self.root)
        pprint(tree_display_dict, width=5, depth=10)


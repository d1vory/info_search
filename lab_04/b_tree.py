from lab_01 import create_words_set


class Node:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BTree:
    def __init__(self, order):
        self.root = Node(True)
        self.order = order

    def printTree(self, root_node, current_level=0):
        print("Level ", current_level, " --> ", len(root_node.keys), end=": ")
        for i in root_node.keys:
            print(i, end=" ")
        print()
        current_level += 1
        if len(root_node.children) > 0:
            for i in root_node.children:
                self.printTree(i, current_level)

    def search(self, key, position: Node=None):
        if position is not None:
            i = 0
            while i < len(position.keys) and key > position.keys[i][0]:
                i += 1
            if i < len(position.keys) and key == position.keys[i][0]:
                return position, i
            elif position.leaf:
                return None
            else:
                # Search its children
                return self.search(key, position.children[i])
        else:
            # Search the entire tree
            return self.search(key, self.root)

    def insert(self, key):
        root = self.root
        # If a node is full, split the child
        if len(root.keys) == (2 * self.order) - 1:
            temp = Node()
            self.root = temp
            temp.children.insert(0, root)
            self._splitChild(temp, 0)
            self._insertNonFull(temp, key)
        else:
            self._insertNonFull(root, key)

    def _insertNonFull(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append((None, None))
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            #i += 1
            if len(node.children[i].keys) == (2 * self.order) - 1:
                self._splitChild(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insertNonFull(node.children[i], key)

    def _splitChild(self, parent_node, child_index):
        y = parent_node.children[child_index]
        z = Node(y.leaf)
        parent_node.children.insert(child_index + 1, z)
        parent_node.keys.insert(child_index, y.keys[self.order - 1])
        z.keys = y.keys[self.order: (2 * self.order) - 1]
        y.keys = y.keys[0: self.order - 1]
        if not y.leaf:
            z.children = y.children[self.order: 2 * self.order]
            y.children = y.children[0: self.order - 1]


def build_tree():
    b_tree = BTree(10)
    for word in create_words_set('../files'):
        b_tree.insert(word)
    return b_tree


tree = build_tree()
tree.printTree(tree.root)

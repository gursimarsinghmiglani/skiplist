from secrets import randbelow


class Node:
    def __init__(self, item=None):
        self.item = item
        self.right = self.up = self.left = self.down = None
        self.width = 1


class SkipListIterator:
    def __init__(self, node):
        if not node.item:
            self.node = node.right
        else:
            self.node = node

    def __iter__(self):
        return self

    def __next__(self):
        if self.node:
            node = self.node
            self.node = self.node.right
            return node.item
        raise StopIteration


class SkipList:
    """
    A dynamic unordered list that supports efficient access, insertion and deletion at arbitrary indices.
    """

    def __init__(self):
        self.topleft = Node()
        self.size = 0

    def __len__(self):
        return self.size

    def raise_error(self, index):
        if not isinstance(index, int):
            raise TypeError("list indices must be integers")
        if 0 > index or index >= len(self):
            raise IndexError("list index out of range")

    def get_node_aux(self, index):
        i = -1
        x = self.topleft
        while True:
            while x.right and i + x.width <= index:
                i += x.width
                x = x.right
            if not x.down:
                break
            x = x.down
        return x

    def get_node(self, index):
        self.raise_error(index)
        return self.get_node_aux(index)

    def __iter__(self):
        x = self.get_node_aux(-1)
        return SkipListIterator(x)

    def __getitem__(self, index):
        x = self.get_node(index)
        return x.item

    def __setitem__(self, index, value):
        x = self.get_node(index)
        x.item = value

    def __delitem__(self, index):
        x = self.get_node(index)
        y = None
        while x:
            x.left.width += x.width - 1
            x.left.right = x.right
            if x.right:
                x.right.left = x.left
            y = x
            x = x.up
        while True:
            while y.left and not y.up:
                y = y.left
            if y.up:
                y.up.width -= 1
                y = y.up
            else:
                break
        self.size -= 1

    def insert(self, index, item):
        if 0 > index or index > len(self):
            raise IndexError("list index out of range")
        x = self.get_node_aux(index - 1)
        y = Node(item)
        y.right = x.right
        x.right = y
        y.left = x
        if y.right:
            y.right.left = y
        while randbelow(2):
            z = Node(item)
            w = y
            width = 0
            while w.left and not w.up:
                w = w.left
                width += w.width
            if w.up:
                z.right = w.up.right
                w.up.right = z
                z.left = w.up
                if z.right:
                    z.right.left = z
                z.width = w.up.width - width + 1
                w.up.width = width
            else:
                topleft = Node()
                topleft.right = z
                z.left = topleft
                self.topleft.up = topleft
                topleft.down = self.topleft
                topleft.width = width
                self.topleft = topleft
            y.up = z
            z.down = y
            y = z
        while True:
            while y.left and not y.up:
                y = y.left
            if y.up:
                y.up.width += 1
                y = y.up
            else:
                break
        self.size += 1

    def append(self, item):
        self.insert(len(self), item)

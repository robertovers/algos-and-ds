import math


class Node():

    def __init__(self, key: int) -> None:
        self.parent: Node = None
        self.key: int = key
        self.degree: int = None

        self.left_child: Node = None
        self.right_sibling: Node = None

    def getOrder(self) -> int:
        return math.log(self.degree, 2)


class BinomialHeap():

    def __init__(self) -> None:
        self.head: Node = None

    @staticmethod
    def mergeTrees(a: Node, b: Node) -> Node:
        if a.key < b.key:
            r_small, r_big = a.root, b.root
        else:
            r_small, r_big = b.root, a.root

        r_big.parent = r_small
        r_big.right_sibling = r_small.left_child
        r_small.left_child = r_big
        r_small.degree += 1
        return r_small

    @staticmethod
    def merge(a: 'BinomialHeap', b: 'BinomialHeap') -> None:
        result = BinomialHeap()

        if a.head and b.head and a.head.getOrder() < b.head.getOrder():
            result.head = a.head
            a.head = a.head.right_sibling
        elif a.head and b.head:
            result.head = b.head
            b.head = b.head.right_sibling

        next = result.head.right_sibling if result.head else result.head

        # phase 1
        while a.head and b.head:
            if a.head.getOrder() < b.head.getOrder():
                next = a.head
                a.head = a.head.right_sibling
            else:
                next = b.head
                b.head = b.head.right_sibling
            next = next.right_sibling

        if next:
            next.right_sibling = a.head or b.head
        else:
            result.head = a.head or b.head

        # phase 2
        x = result.head
        next_x = result.head.right_sibling
        prev_x = None

        while next_x:
            order_x = x.getOrder()
            if next_x.getOrder() != order_x:
                x = x.right_sibling
                next_x = next_x.right_sibling
                prev_x = prev_x.right_sibling if prev_x else result.head
            elif next_x.getOrder() == order_x and next_x.right_sibling.getOrder() != order_x:
                x = BinomialHeap.mergeTrees(x, next_x)
                if prev_x:
                    prev_x.right_sibling = x
                next_x = x.right_sibling
            else:
                x = x.right_sibling
                next_x = next_x.right_sibling
                prev_x = prev_x.right_sibling if prev_x else result.head

        return result

    def min(self) -> int:
        cur_min = self.head
        current = self.head
        while current:
            if current.key < cur_min.key:
                cur_min = current
            current = current.right_sibling
        return cur_min.key

    def extractMin(self) -> int:
        # find min node in root list
        cur_min = self.head
        current = self.head
        prev = None
        while current:
            if current.key < cur_min.key:
                cur_min = current
            current = current.right_sibling
            prev = current
        if prev:
            prev.right_sibling = None

        # reverse children of min node
        prev = None
        current = cur_min.left_child
        while current:
            next = current.right_sibling
            current.right_sibling = prev
            prev = current
            current = next
        children_head = prev

        # merge heaps
        self = BinomialHeap.merge(self.head, children_head)

        # return min
        return cur_min.key

    def insert(self, x: int) -> None:
        new_item = BinomialHeap()
        new_item.head = Node(x)
        self = BinomialHeap.merge(self, new_item)

    def decreaseKey(self, a: Node, new_key: int) -> None:
        a.key = new_key
        while a.key < a.parent.key:
            temp = a.key
            a.key = a.parent.key
            a.parent.key = temp

    def delete(self, a: Node) -> None:
        self.decreaseKey(a, -math.inf)
        self.extractMin()

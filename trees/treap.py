import random
from typing import Union


class RandomizedTreapNode:
    """
    Represents a node within a Randomized Treap data structure.
    """

    def __init__(self, key: int, prio: float | None = None) -> None:
        """
        Given a data element, instantiates the node with a priority drawn from
        a continuous, uniform distribution over the range (0, 1).
        """
        self.key = key
        self.prio: float = random.random() if not prio else prio

        self.parent: 'RandomizedTreapNode' | None = None
        self.left: 'RandomizedTreapNode' | None = None
        self.right: 'RandomizedTreapNode' | None = None

    def _assert_correctness(self) -> None:
        """
        Asserts the correctness of the subtree rooted at this node, that is:
            - Its children have a priority greater than its own;
            - Its left child has a search key less than its own;
            - Its right child has a search key greater than its own;
            - The pointers are correct between parent and child; and
            - Its left and right subtrees have a correct structure.
        """
        if self.left:
            assert self.left.parent == self
            assert self.left.prio >= self.prio
            assert self.left.key < self.key
            self.left._assert_correctness()
        if self.right:
            assert self.right.parent == self
            assert self.right.prio >= self.prio
            assert self.right.key > self.key
            self.right._assert_correctness()

    def insert(self, n_node: 'RandomizedTreapNode') -> None:
        """
        Inserts a new node (n_node) into the sub-treap rooted at this node.
        """
        n_key = n_node.key
        if n_key < self.key or n_key == self.key:
            if not self.left:
                self.left = n_node
                self.left.parent = self
                return
            self.left.insert(n_node)
        elif n_key > self.key or n_key == self.key:
            if not self.right:
                self.right = n_node
                self.right.parent = self
                return
            self.right.insert(n_node)

    def search(self, s_key: int) -> Union['RandomizedTreapNode', None]:
        """
        Searches for a key (s_key) in the sub-treap rooted at this node.

        Returns: A node with key = s_key if found, else None.
        """
        if s_key == self.key:
            return self
        elif s_key < self.key:
            if self.left:
                return self.left.search(s_key)
            return None
        else:
            if self.right:
                return self.right.search(s_key)
            return None

    def min_child(self) -> Union['RandomizedTreapNode', None]:
        if self.left and self.right:
            if self.left.prio < self.right.prio:
                return self.left
            return self.right
        return self.left or self.right


class RandomizedTreap:

    def __init__(self) -> None:
        """
        Instantiates the treap with an empty root node.
        """
        self.root: RandomizedTreapNode | None = None

    def _assert_correctness(self) -> None:
        """
        Asserts the correctness of the treap's properties, i.e:
            - A valid BST over its search keys,
            - A valid min-heap over its priorities.
        """
        if self.root:
            self.root._assert_correctness()
    
    def insert(self, n_elt: int) -> None:
        """
        Inserts a new element (n_elt) into the treap.
        It does this by calling the insert method of the root node
        if it exists, if not it sets the element as the root.

        Time: O(logn)
        """
        if not self.root:
            self.root = RandomizedTreapNode(n_elt)
            return

        n_node = RandomizedTreapNode(n_elt)
        self.root.insert(n_node)
        self.restore_heap_insertion(n_node)

    def search(self, s_key: int) -> RandomizedTreapNode | None:
        """
        Searches for a search key (s_key) in the treap.

        Returns: A node with key = s_key if found, else None.
        Time: O(logn)
        """
        if self.root:
            return self.root.search(s_key)
        return None

    def delete(self, d_key: int) -> None:
        """
        Deletes a search key (d_key) from the treap if found.

        Time: O(logn)
        """
        d_node = self.search(d_key)
        if not d_node:
            return
        d_node.prio = float("inf")
        if d_node.left or d_node.right:
            d_node = self.restore_heap_deletion(d_node)
        self.delete_leaf(d_node)

    def restore_heap_insertion(self, r_node: RandomizedTreapNode) -> None:
        """
        Performs rotations from a given node (r_node) until the heap invariant
        is restored, i.e. no child has a smaller priority than its parent.

        Time: O(logn)
        """
        while r_node.parent and r_node.prio < r_node.parent.prio:

            grandparent = r_node.parent.parent

            if r_node == r_node.parent.left:
                r_node = self.rotate_right(r_node)
            else:
                r_node = self.rotate_left(r_node)

            if self.root == r_node.parent:
                # if parent was root, update the root
                self.root = r_node
                r_node.parent = None
            elif grandparent:
                # otherwise update grandparent's pointers
                r_node.parent = grandparent
                if r_node.key < grandparent.key or r_node.key == grandparent.key:
                    grandparent.left = r_node
                else:
                    grandparent.right = r_node

    def restore_heap_deletion(self, d_node: RandomizedTreapNode) -> RandomizedTreapNode:
        """
        Performs rotations from a given node being deleted (d_node) until the heap
        invariant is restored, i.e. no child has a smaller priority than its parent.

        Time: O(logn)
        """
        while d_node.left or d_node.right:

            # rotate d_node with its smaller child
            r_node = d_node.min_child()
            grandparent = r_node.parent.parent

            if r_node == r_node.parent.left:
                r_node = self.rotate_right(r_node)
            else:
                r_node = self.rotate_left(r_node)

            if self.root == r_node.parent:
                # if parent was root, update the root
                self.root = r_node
                r_node.parent = None
            elif grandparent:
                # otherwise update grandparent's pointers
                r_node.parent = grandparent
                if r_node.key < grandparent.key or r_node.key == grandparent.key and r_node.id < grandparent.id:
                    grandparent.left = r_node
                else:
                    grandparent.right = r_node
        
        return d_node

    def rotate_left(self, r_node: RandomizedTreapNode) -> RandomizedTreapNode:
        """
        Rotates a right child node (r_node) with its parent.
        Time: O(1)
        Returns: The sub-treap rooted at r_node.
        """
        temp = r_node.left
        r_node.left = r_node.parent
        r_node.left.parent = r_node
        r_node.left.right = temp
        if temp:
            temp.parent = r_node.left
        return r_node

    def rotate_right(self, r_node: RandomizedTreapNode) -> RandomizedTreapNode:
        """
        Rotates a left child node (r_node) with its parent.
        Returns: The sub-treap rooted at r_node.
        Time: O(1)
        """
        temp = r_node.right
        r_node.right = r_node.parent
        r_node.right.parent = r_node
        r_node.right.left = temp
        if temp:
            temp.parent = r_node.right
        return r_node

    def delete_leaf(self, d_node: RandomizedTreapNode) -> None:
        """
        Deletes a leaf node (d_node) from the treap.
        Time: O(1)
        """
        if d_node == self.root:
            self.root = None
        elif d_node.parent.left == d_node:
            d_node.parent.left = None
        else:
            d_node.parent.right = None
        del d_node

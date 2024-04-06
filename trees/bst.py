from typing import List


class BSTNode:

    def __init__(self, key: int) -> None:
        self.key: int = key
        self.left_child: BSTNode | None = None
        self.right_child: BSTNode | None = None

    def insert(self, key: int) -> None:
        if key < self.key:
            if self.left_child:
                self.left_child.insert(key)
                return
            self.left_child = BSTNode(key)
        else:
            if self.right_child:
                self.right_child.insert(key)
                return
            self.right_child = BSTNode(key)

    def search(self, key: int) -> bool:
        if key == self.key:
            return True
        elif key < self.key:
            if not self.left_child:
                return False
            return self.left_child.search(key)
        else:
            if not self.right_child:
                return False
            return self.right_child.search(key)


class BinarySearchTree:
    
    def __init__(self) -> None:
        self.head: BSTNode | None = None
    
    def insert(self, key: int) -> None:
        """
        Inserts a key into the BST.

        Time: O(n)
        """
        if not self.head:
            self.head = BSTNode(key)
        self.head.insert(key)

    def search(self, key: int) -> bool:
        """
        Searches for a key in the BST.

        Time: O(n)
        """
        if not self.head:
            return False
        return self.head.search(key)


if __name__ == "__main__":

    bst = BinarySearchTree()
    bst.insert(2)
    bst.insert(6)
    bst.insert(8)
    bst.insert(9)
    bst.insert(5)

    print(bst.search(2))
    print(bst.search(5))
    print(bst.search(3))

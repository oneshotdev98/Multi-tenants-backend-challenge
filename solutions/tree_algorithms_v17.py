#!/usr/bin/env python3
"""Tree Data Structures and Algorithms"""

class TreeNode:
    """Binary tree node"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    """Binary Search Tree implementation"""
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Insert value into BST"""
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """Recursive helper for insert"""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def inorder(self, node=None):
        """In-order traversal (Left, Root, Right)"""
        if node is None:
            node = self.root
        result = []
        if node:
            result.extend(self.inorder(node.left))
            result.append(node.value)
            result.extend(self.inorder(node.right))
        return result

    def preorder(self, node=None):
        """Pre-order traversal (Root, Left, Right)"""
        if node is None:
            node = self.root
        result = []
        if node:
            result.append(node.value)
            result.extend(self.preorder(node.left))
            result.extend(self.preorder(node.right))
        return result

    def postorder(self, node=None):
        """Post-order traversal (Left, Right, Root)"""
        if node is None:
            node = self.root
        result = []
        if node:
            result.extend(self.postorder(node.left))
            result.extend(self.postorder(node.right))
            result.append(node.value)
        return result

    def height(self, node=None):
        """Calculate tree height"""
        if node is None:
            node = self.root
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

if __name__ == "__main__":
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]

    for val in values:
        bst.insert(val)

    print(f"In-order: {bst.inorder()}")
    print(f"Pre-order: {bst.preorder()}")
    print(f"Post-order: {bst.postorder()}")
    print(f"Tree height: {bst.height()}")

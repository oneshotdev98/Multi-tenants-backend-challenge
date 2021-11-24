#!/usr/bin/env python3
"""Basic Data Structure Implementations"""

class Stack:
    """LIFO (Last In First Out) Stack Implementation"""
    def __init__(self):
        self.items = []

    def push(self, item):
        """Add item to top of stack"""
        self.items.append(item)

    def pop(self):
        """Remove and return top item"""
        return self.items.pop() if not self.is_empty() else None

    def peek(self):
        """View top item without removing"""
        return self.items[-1] if not self.is_empty() else None

    def is_empty(self):
        """Check if stack is empty"""
        return len(self.items) == 0

    def size(self):
        """Get stack size"""
        return len(self.items)

class Queue:
    """FIFO (First In First Out) Queue Implementation"""
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Add item to rear of queue"""
        self.items.append(item)

    def dequeue(self):
        """Remove and return front item"""
        return self.items.pop(0) if not self.is_empty() else None

    def is_empty(self):
        """Check if queue is empty"""
        return len(self.items) == 0

    def size(self):
        """Get queue size"""
        return len(self.items)

class LinkedListNode:
    """Node for linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Singly Linked List Implementation"""
    def __init__(self):
        self.head = None

    def insert(self, data):
        """Insert at beginning"""
        new_node = LinkedListNode(data)
        new_node.next = self.head
        self.head = new_node

    def search(self, data):
        """Search for value"""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    def display(self):
        """Print all elements"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements) if elements else "Empty"

if __name__ == "__main__":
    # Test Stack
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"Stack: {stack.items}")

    # Test Queue
    queue = Queue()
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")
    print(f"Queue: {queue.items}")

    # Test LinkedList
    ll = LinkedList()
    ll.insert(3)
    ll.insert(2)
    ll.insert(1)
    print(f"LinkedList: {ll.display()}")

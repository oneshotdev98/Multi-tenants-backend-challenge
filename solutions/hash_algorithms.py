#!/usr/bin/env python3
"""Hash Table and Hash Function Implementations"""

class HashTable:
    """Hash table using separate chaining"""
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        """Hash function"""
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert key-value pair"""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def search(self, key):
        """Search for key"""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Delete key-value pair"""
        index = self._hash(key)
        self.table[index] = [(k, v) for k, v in self.table[index] if k != key]

def find_duplicates(arr):
    """Find duplicate elements in array"""
    seen = {}
    duplicates = []

    for num in arr:
        if num in seen:
            seen[num] += 1
        else:
            seen[num] = 1

    for num, count in seen.items():
        if count > 1:
            duplicates.append(num)

    return duplicates

def two_sum(arr, target):
    """Find two numbers that sum to target"""
    seen = {}
    for num in arr:
        complement = target - num
        if complement in seen:
            return [complement, num]
        seen[num] = True
    return None

if __name__ == "__main__":
    # Test HashTable
    ht = HashTable()
    ht.insert("name", "Alice")
    ht.insert("age", 30)
    print(f"Search 'name': {ht.search('name')}")

    # Test duplicates
    print(f"Duplicates in [1,2,2,3,3,3]: {find_duplicates([1, 2, 2, 3, 3, 3])}")

    # Test two sum
    print(f"Two sum [2,7,11,15], target 9: {two_sum([2, 7, 11, 15], 9)}")

#!/usr/bin/env python3
"""Search Algorithm Implementations"""

def linear_search(arr, target):
    """Linear search - O(n) time complexity"""
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1

def binary_search(arr, target):
    """Binary search - O(log n) time complexity (requires sorted array)"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

def binary_search_recursive(arr, target, left=0, right=None):
    """Recursive binary search"""
    if right is None:
        right = len(arr) - 1

    if left > right:
        return -1

    mid = (left + right) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)

def interpolation_search(arr, target):
    """Interpolation search - O(log log n) average case"""
    left, right = 0, len(arr) - 1

    while left <= right and arr[left] <= target <= arr[right]:
        pos = left + int((right - left) / (arr[right] - arr[left]) * (target - arr[left]))

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1

    return -1

if __name__ == "__main__":
    arr = [2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78]
    target = 23

    print(f"Array: {arr}")
    print(f"Target: {target}")
    print(f"Linear Search: {linear_search(arr, target)}")
    print(f"Binary Search: {binary_search(arr, target)}")
    print(f"Binary Search (Recursive): {binary_search_recursive(arr, target)}")
    print(f"Interpolation Search: {interpolation_search(arr, target)}")

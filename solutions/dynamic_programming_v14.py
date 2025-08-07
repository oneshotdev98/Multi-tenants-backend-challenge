#!/usr/bin/env python3
"""Dynamic Programming Solutions"""

def fibonacci(n, memo={}):
    """Fibonacci with memoization"""
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]

def coin_change(coins, amount):
    """Minimum coins for amount"""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

def longest_increasing_subsequence(arr):
    """Find LIS length"""
    n = len(arr)
    if n == 0:
        return 0

    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

def knapsack_01(weights, values, capacity):
    """0/1 Knapsack problem"""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]

if __name__ == "__main__":
    print(f"Fibonacci(10): {fibonacci(10)}")
    print(f"Coin change [1,2,5] for 5: {coin_change([1, 2, 5], 5)}")
    print(f"LIS of [10,9,2,5,3,7,101,18]: {longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])}")
    print(f"Knapsack(weights=[2,3,4,5], values=[3,4,5,6], capacity=5): {knapsack_01([2, 3, 4, 5], [3, 4, 5, 6], 5)}")

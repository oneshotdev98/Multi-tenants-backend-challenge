#!/usr/bin/env python3
"""String Algorithm Implementations"""

def is_palindrome(s):
    """Check if string is palindrome"""
    clean = ''.join(c.lower() for c in s if c.isalnum())
    return clean == clean[::-1]

def kmp_search(text, pattern):
    """Knuth-Morris-Pratt (KMP) string matching"""
    def build_lps(pattern):
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(text)
    m = len(pattern)
    lps = build_lps(pattern)
    i = j = 0
    matches = []

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches

def anagram(s1, s2):
    """Check if two strings are anagrams"""
    return sorted(s1.lower()) == sorted(s2.lower())

def longest_common_substring(s1, s2):
    """Find longest common substring"""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    end_pos = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i

    return s1[end_pos - max_len:end_pos] if max_len > 0 else ""

if __name__ == "__main__":
    print(f"Is 'racecar' palindrome? {is_palindrome('racecar')}")
    print(f"KMP search 'ABABDABACDABABCABAB' for 'ABABCABAB': {kmp_search('ABABDABACDABABCABAB', 'ABABCABAB')}")
    print(f"Are 'listen' and 'silent' anagrams? {anagram('listen', 'silent')}")
    print(f"LCS of 'ABCDGH' and 'AEDFHR': {longest_common_substring('ABCDGH', 'AEDFHR')}")

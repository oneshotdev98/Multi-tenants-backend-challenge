#!/usr/bin/env python3
"""Matrix Operations and Algorithms"""

def matrix_multiply(A, B):
    """Multiply two matrices"""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])

    if cols_A != rows_B:
        raise ValueError("Incompatible dimensions")

    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result

def transpose(matrix):
    """Transpose a matrix"""
    rows = len(matrix)
    cols = len(matrix[0])
    return [[matrix[i][j] for i in range(rows)] for j in range(cols)]

def determinant(matrix):
    """Calculate determinant of square matrix"""
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += ((-1) ** j) * matrix[0][j] * determinant(minor)

    return det

def rotate_matrix_90(matrix):
    """Rotate matrix 90 degrees clockwise"""
    n = len(matrix)
    matrix = transpose(matrix)
    for row in matrix:
        row.reverse()
    return matrix

if __name__ == "__main__":
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]

    print(f"Matrix A:\n{A}")
    print(f"Matrix B:\n{B}")
    print(f"A * B:\n{matrix_multiply(A, B)}")

    M = [[1, 2], [3, 4]]
    print(f"Transpose of {M}: {transpose(M)}")
    print(f"Determinant of {M}: {determinant(M)}")

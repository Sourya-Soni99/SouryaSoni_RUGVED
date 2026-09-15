def rot90_CW(matrix):
    n = len(matrix)
    rotated = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rotated[j][n - 1 - i] = matrix[i][j]
    return rotated


def spiralOrder(matrix):
    if not matrix:
        return []

    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    result = []

    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1

        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1

        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1

        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1

    return result

n = int(input("Enter size N for N x N matrix: "))
print("Enter elements row by row (space separated):")
matrix = []
for i in range(n):
    row = list(map(int, input(f"Row {i+1}: ").split()))
    matrix.append(row)

rotated = rot90_CW(matrix)
print("\nRotated 90° Clockwise Matrix:")
for row in rotated:
    print(row)

spiral = spiralOrder(matrix)
print("\nElements in Spiral Order:", spiral)
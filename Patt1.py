def diamondPatt(n):
    print(f"\nDiamond Pattern (N = {n}):")
    for i in range(1, n + 1):
        print(" " * (n - i) + " ".join(["*"] * i))
    for i in range(n - 1, 0, -1):
        print(" " * (n - i) + " ".join(["*"] * i))

def butterflyPatt(n):
    print(f"\nButterfly Pattern (N = {n}):")
    for i in range(1, n + 1):
        stars = "* " * i
        spaces = "  " * (2 * (n - i))
        print(stars.strip() + " " + spaces + stars.strip())
    for i in range(n, 0, -1):
        stars = "* " * i
        spaces = "  " * (2 * (n - i))
        print(stars.strip() + " " + spaces + stars.strip())

n = int(input("Enter size N for patterns: "))
diamondPatt(n)
butterflyPatt(n)
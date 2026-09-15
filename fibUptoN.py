def printFib(n):
    if n <= 0:
        print("Please enter a positive integer.")
        return
    a, b = 0, 1
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    print("Fibonacci Sequence:", seq)

n = int(input("Enter number of values (n): "))
printFib(n)
def isHill(str):
    if len(str) < 3:
        return False
    i = 0
    while i < len(str) - 1 and str[i] < str[i + 1]:
        i += 1
    if i == 0 or i == len(str) - 1:
        return False
    while i < len(str) - 1 and str[i] > str[i + 1]:
        i += 1
    return i == len(str) - 1

num = input("Enter a number to check if it's a hill number: ").strip()
if isHill(num):
    print(f"{num} is a Hill Number.")
else:
    print(f"{num} is NOT a Hill Number.")
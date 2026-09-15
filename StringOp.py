def sortAndCount(s):
    str = "".join(sorted(s))
    counts = {}
    for char in str:
        counts[char] = counts.get(char, 0) + 1
    print(f"Sorted String: {str}")
    print("Character Counts:")
    for char, count in counts.items():
        print(f"'{char}': {count}")

s = input("Enter a string: ")
sortAndCount(s)